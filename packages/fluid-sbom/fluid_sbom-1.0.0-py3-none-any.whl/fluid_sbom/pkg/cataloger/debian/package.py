from bs4 import (
    BeautifulSoup,
    Tag,
)
from contextlib import (
    suppress,
)
from copy import (
    deepcopy,
)
from fluid_sbom import (
    advisories,
)
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.internal.file_resolver.container_image import (
    ContainerImage,
)
from fluid_sbom.internal.package_information.debian import (
    get_deb_package_version_list,
    get_deb_snapshot,
)
from fluid_sbom.linux.release import (
    Release,
)
from fluid_sbom.pkg.cataloger.debian.parse_copyright import (
    parse_licenses_from_copyright,
)
from fluid_sbom.pkg.cataloger.debian.parse_dpkg_info_files import (
    parse_dpkg_conffile_info,
    parse_dpkg_md5_info,
)
from fluid_sbom.pkg.dpkg import (
    DpkgDBEntry,
    DpkgFileRecord,
)
from fluid_sbom.pkg.language import (
    Language,
)
from fluid_sbom.pkg.package import (
    Artifact,
    HealthMetadata,
    Package,
)
from fluid_sbom.pkg.type import (
    PackageType,
)
from fluid_sbom.pkg.url import (
    purl_qualifiers,
)
from fluid_sbom.utils.file import (
    Digest,
)
import logging
import os
from packageurl import (
    PackageURL,
)
from pathlib import (
    Path,
)
from pydantic import (
    ValidationError,
)
from typing import (
    cast,
    TextIO,
)

LOGGER = logging.getLogger(__name__)


def package_url(pkg: DpkgDBEntry, distro: Release | None = None) -> str | None:
    if distro is None:
        return None
    if distro.id_ != "debian" and "debian" not in (distro.id_like or []):
        return ""
    qualifiers = {"arch": pkg.architecture}
    if pkg.source:
        if pkg.source_version:
            qualifiers["upstream"] = f"{pkg.source}@{pkg.source_version}"
        else:
            qualifiers["upstream"] = pkg.source

    return PackageURL(
        type="deb",
        namespace=distro.id_,
        name=pkg.package,
        version=pkg.version,
        qualifiers=purl_qualifiers(qualifiers, distro),
        subpath="",
    ).to_string()


def md5_key(metadata: DpkgDBEntry) -> str:
    content_key = metadata.package
    if metadata.architecture not in ("", "all"):
        return f"{content_key}:{metadata.architecture}"
    return content_key


def fetch_md5_content(
    resolver: Resolver, db_location: Location, entry: DpkgDBEntry
) -> tuple[TextIO | None, Location | None] | None:
    if not db_location.coordinates:
        return None
    search_path = str(Path(db_location.coordinates.real_path).parent)
    if not search_path.endswith("status.d"):
        search_path = os.path.join(search_path, "info")
    name = md5_key(entry)
    location = resolver.relative_file_path(
        db_location, os.path.join(search_path, name + ".md5sums")
    )
    if not location:
        location = resolver.relative_file_path(
            db_location, os.path.join(search_path, entry.package + ".md5sums")
        )
    if not location:
        return None

    reader = resolver.file_contents_by_location(location)
    if not reader:
        LOGGER.warning(
            "failed to fetch deb md5 contents (package=%s)",
            entry.package,
        )
    return reader, location


def fetch_conffile_contents(
    resolver: Resolver, db_location: Location, entry: DpkgDBEntry
) -> tuple[TextIO | None, Location | None] | None:
    if not db_location.coordinates:
        return None
    parent_path = str(Path(db_location.coordinates.real_path).parent)

    name = md5_key(entry)
    location = resolver.relative_file_path(
        db_location, os.path.join(parent_path, "info", name + ".conffiles")
    )
    if not location:
        location = resolver.relative_file_path(
            db_location,
            os.path.join(parent_path, "info", entry.package + ".conffiles"),
        )
    if not location:
        return None, None
    reader = resolver.file_contents_by_location(location)
    if not reader:
        LOGGER.warning(
            "failed to fetch deb conffiles contents (package=%s)",
            entry.package,
        )
    return reader, location


def get_additional_file_listing(
    resolver: Resolver, db_location: Location, entry: DpkgDBEntry
) -> tuple[list[DpkgFileRecord], list[Location]]:
    files: list[DpkgFileRecord] = []
    locations: list[Location] = []
    md5_result = fetch_md5_content(resolver, db_location, entry)
    if not md5_result:
        return files, locations
    md5_reader, md5_location = md5_result
    if md5_reader is not None and md5_location is not None:
        files.extend(parse_dpkg_md5_info(md5_reader))
        locations.append(md5_location)
    conffiles = fetch_conffile_contents(resolver, db_location, entry)
    if not conffiles:
        return files, locations
    conffiles_reader, conffiles_location = conffiles

    if conffiles_reader is not None and conffiles_location is not None:
        files.extend(parse_dpkg_conffile_info(conffiles_reader))
        locations.append(conffiles_location)

    return files, locations


def merge_file_listing(
    resolver: Resolver, db_location: Location, pkg: Package
) -> None:
    metadata: DpkgDBEntry = cast(DpkgDBEntry, pkg.metadata)
    files, info_locations = get_additional_file_listing(
        resolver, db_location, metadata
    )
    for new_file in files:
        exists = False
        for existing_file in metadata.files or []:
            if existing_file.path == new_file.path:
                exists = True
                break
        if not exists and metadata.files:
            metadata.files.append(new_file)
    sorted_files = sorted(metadata.files or [], key=lambda x: x.path)
    metadata.files = sorted_files
    pkg.metadata = metadata
    pkg.locations.extend(info_locations)


def fetch_copyright_contents(
    resolver: Resolver | None, db_location: Location, metadata: DpkgDBEntry
) -> tuple[TextIO | None, Location | None]:
    if not resolver:
        return None, None

    copyright_path = os.path.join(
        "/usr/share/doc", metadata.package, "copyright"
    )
    location = resolver.relative_file_path(db_location, copyright_path)

    if not location:
        return None, None

    reader = resolver.file_contents_by_location(location)
    if not reader:
        LOGGER.warning(
            "failed to fetch deb copyright contents (package=%s)",
            metadata.package,
        )

    return reader, location


def add_licenses(
    resolver: Resolver, db_location: Location, pkg: Package
) -> None:
    metadata: DpkgDBEntry = cast(DpkgDBEntry, pkg.metadata)

    pkg.licenses = []
    copyright_reader, copyright_location = fetch_copyright_contents(
        resolver, db_location, metadata
    )

    if copyright_reader is not None and copyright_location is not None:
        licenses_strs = parse_licenses_from_copyright(copyright_reader)
        pkg.licenses = licenses_strs


def new_dpkg_package(
    entry: DpkgDBEntry,
    db_location: Location,
    _resolver: Resolver | None,
    release: Release | None = None,
) -> Package | tuple[Package, Package] | None:
    try:
        dpkg = Package(
            name=entry.package,
            version=entry.version or "",
            licenses=[],
            p_url=package_url(entry, release),
            locations=[db_location],
            type=PackageType.DebPkg,
            metadata=entry,
            found_by=None,
            language=Language.UNKNOWN_LANGUAGE,
        )
        arch: str | None = None
        if _resolver is not None:
            # side effects
            merge_file_listing(_resolver, db_location, dpkg)
            add_licenses(_resolver, db_location, dpkg)
            if isinstance(_resolver, ContainerImage):
                arch = _resolver.context.arch
        source_dpkg: Package | None = None
        if (entry.source and entry.source != dpkg.name) or (
            entry.source
            and entry.source_version
            and entry.source_version != dpkg.version
        ):
            new_entry = deepcopy(entry)
            new_entry.package = entry.source
            new_entry.version = entry.source_version or dpkg.version
            new_entry.source = None
            new_entry.source_version = None
            new_entry.dependencies = None
            new_entry.pre_dependencies = None

            source_dpkg = deepcopy(dpkg)
            source_dpkg.name = new_entry.package
            source_dpkg.version = new_entry.version
            source_dpkg.p_url = package_url(new_entry, release)

            source_dpkg = complete_package(source_dpkg, release, arch)

        dpkg = complete_package(dpkg, release, arch)
        if source_dpkg:
            return dpkg, source_dpkg
        return dpkg
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data types "
            "are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),
                    "location": db_location.path(),
                }
            },
        )
        return None


def _search_download_url(
    package: Package, arch: str | None = None
) -> tuple[str, str | None] | None:
    html_download = get_deb_snapshot(package.name, package.version)
    if not html_download:
        return None
    parsed = BeautifulSoup(html_download, features="html.parser")
    tags: list[Tag] = parsed.find_all("a", href=True)
    tag_href: str | None = None
    for tag in tags:
        tag = cast(Tag, tag)
        if (
            tag.text.endswith(".deb")
            and package.name in tag.text
            and package.version in tag.text
            and (arch in tag.text if arch else True)
        ):
            tag_href = tag.get("href")
            break
    else:
        for tag in tags:
            tag = cast(Tag, tag)
            if (
                tag.text.endswith(".deb")
                and package.name in tag.text
                and package.version in tag.text
            ):
                tag_href = tag.get("href")
                break
    if not tag_href:
        return None
    sha1_hash: str | None = None
    with suppress(IndexError):
        sha1_hash = list(tag.fetchPrevious("code", limit=1))[0].text

    return f"https://snapshot.debian.org{tag_href}", sha1_hash


def complete_package(
    package: Package, release: Release | None = None, arch: str | None = None
) -> Package:
    pkg_advisories = advisories.get_package_advisories(package)
    if pkg_advisories:
        package.advisories = pkg_advisories
    version_code_name: str | None = None
    if release:
        version_code_name = release.version_code_name
    versions_list = get_deb_package_version_list(
        package.name, version_code_name
    )
    package.health_metadata = HealthMetadata()
    if versions_list:
        package.health_metadata = HealthMetadata(
            latest_version=versions_list[0]["version"],
        )
    if package.metadata and hasattr(package.metadata, "maintainer"):
        package.health_metadata.authors = package.metadata.maintainer
    download_url_item = _search_download_url(package, arch)
    if download_url_item:
        digest_value = download_url_item[1] or None
        package.health_metadata.artifact = Artifact(
            url=download_url_item[0],
            integrity=Digest(
                algorithm="sha1" if digest_value else None, value=digest_value
            ),
        )
    return package
