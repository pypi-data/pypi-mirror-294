from bs4 import (
    BeautifulSoup,
    Tag,
)
from contextlib import (
    suppress,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.internal.package_information.alpine import (
    get_package_versions_html,
)
from fluid_sbom.linux.release import (
    Release,
)
from fluid_sbom.pkg.apk import (
    ApkDBEntry,
)
from fluid_sbom.pkg.language import (
    Language,
)
from fluid_sbom.pkg.package import (
    HealthMetadata,
    Package,
)
from fluid_sbom.pkg.type import (
    PackageType,
)
import logging
from packageurl import (
    PackageURL,
)
from pydantic import (
    ValidationError,
)

LOGGER = logging.getLogger(__name__)


@dataclass
class ParsedData:
    apk_db_entry: ApkDBEntry
    license: str


def package_url(
    entry: ApkDBEntry | None, distro: Release | None
) -> str | None:
    if not entry or not distro:
        return None
    qualifiers = {"arch": entry.architecture or ""}
    if entry.origin_package != entry.package and entry.origin_package:
        qualifiers["upstream"] = entry.origin_package
    distro_qualifiers = []
    if distro.id_:
        distro_qualifiers.append(distro.id_)
    if distro.version_id:
        distro_qualifiers.append(distro.version_id)
    elif distro.build_id:
        distro_qualifiers.append(distro.build_id)
    if distro_qualifiers:
        qualifiers["distro"] = "-".join(distro_qualifiers)
    return PackageURL(
        type="apk",
        namespace=distro.id_.lower(),
        name=entry.package,
        version=entry.version,
        qualifiers=qualifiers,
        subpath="",
    ).to_string()


def new_package(
    data: ParsedData,
    release: Release | None,
    db_location: Location,
    arch: str | None = None,
) -> Package | None:
    try:
        package = Package(
            name=data.apk_db_entry.package,
            version=data.apk_db_entry.version,
            locations=[db_location],
            licenses=data.license.split(" "),
            p_url=package_url(data.apk_db_entry, release),
            type=PackageType.ApkPkg,
            metadata=data.apk_db_entry,
            found_by=None,
            health_metadata=None,
            language=Language.UNKNOWN_LANGUAGE,
        )
        package = complete_package(
            package, release.version_id if release else None, arch
        )
        return package if package else None
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data "
            "types are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),
                    "location": db_location.path(),
                }
            },
        )
        return None


def complete_package(
    package: Package,
    distro_version: str | None = None,
    arch: str | None = None,
) -> Package:
    package.health_metadata = HealthMetadata()
    if package.metadata and hasattr(package.metadata, "maintainer"):
        package.health_metadata.authors = package.metadata.maintainer
    html_content = get_package_versions_html(
        package.name, distro_version, arch
    )
    if not html_content:
        return package

    parsed_content = BeautifulSoup(html_content, features="html.parser")
    version_items: list[Tag] = list(
        parsed_content.find_all("td", {"class": "version"})
    )
    if version_items:
        latest_version = version_items[0].text.strip()
        package.health_metadata.latest_version = latest_version
        with suppress(IndexError):
            parent_tr: Tag = list(
                version_items[0].fetchPrevious("tr", limit=1)
            )[0]
            if build_date_tag := parent_tr.find_next("td", {"class": "bdate"}):
                package.health_metadata.latest_version_created_at = (
                    datetime.fromisoformat(build_date_tag.text.strip())
                )
    return package
