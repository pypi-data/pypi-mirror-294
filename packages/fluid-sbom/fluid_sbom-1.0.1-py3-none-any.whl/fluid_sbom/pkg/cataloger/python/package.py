from fluid_sbom import (
    advisories,
)
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.internal.package_information.python import (
    get_pypi_package,
)
from fluid_sbom.pkg.cataloger.python.parse_wheel_egg_metadata import (
    ParsedData,
)
from fluid_sbom.pkg.language import (
    Language,
)
from fluid_sbom.pkg.package import (
    Artifact,
    HealthMetadata,
    Package,
)
from fluid_sbom.pkg.python import (
    PythonPackage,
)
from fluid_sbom.pkg.type import (
    PackageType,
)
from fluid_sbom.utils.file import (
    Digest,
)
import logging
from packageurl import (
    PackageURL,
)
from pydantic import (
    ValidationError,
)
from typing import (
    Any,
)

LOGGER = logging.getLogger(__name__)


class UnexpectedValueType(Exception):
    pass


def new_package_for_package(
    _resolver: Resolver, data: ParsedData, sources: Location
) -> Package | None:
    try:
        return Package(
            name=data.python_package.name,
            version=data.python_package.version or "",
            p_url=package_url(
                data.python_package.name,
                data.python_package.version or "",
                data.python_package,
            ),
            locations=[sources],
            language=Language.PYTHON,
            type=PackageType.PythonPkg,
            metadata=data.python_package,
            licenses=[data.licenses],
        )
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data types "
            "are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),
                    "location": sources.path(),
                }
            },
        )
        return None


def package_url(name: str, version: str, package: PythonPackage | None) -> str:
    return PackageURL(
        type="pypi",
        namespace="",
        name=name,
        version=version,
        qualifiers=_purl_qualifiers_for_package(package),
        subpath="",
    ).to_string()


def _purl_qualifiers_for_package(
    package: PythonPackage | None,
) -> dict[str, str]:
    if not package:
        return {}
    if package.direct_url_origin and package.direct_url_origin.vcs:
        url = package.direct_url_origin
        return {"vcs_url": f"{url.vcs}+{url.url}@{url.commit_id}"}
    return {}


def _set_health_metadata_artifact(
    *,
    package: Package,
    current_package: dict[str, Any] | None,
) -> Package:
    if not current_package or not package.health_metadata:
        return package

    if url := next(
        (x for x in current_package["urls"] if x["url"].endswith(".tar.gz")),
        None,
    ):
        digest_value = url.get("digests", {}).get("sha256") or None
        package.health_metadata.artifact = Artifact(
            url=url.get("url"),
            integrity=Digest(
                algorithm="sha256" if digest_value else None,
                value=digest_value,
            ),
        )
    else:
        package.health_metadata.artifact = Artifact(
            url=f"https://pypi.org/pypi/{package.name}",
        )
    return package


def _set_authors(
    *,
    package: Package,
    pypi_package: dict[str, Any],
) -> Package:
    package_info = pypi_package["info"]
    if package.health_metadata and "author" in package_info:
        author: str | None = None
        package_author = package_info["author"]
        author_email = package_info.get("author_email")
        if isinstance(package_author, str) and package_author:
            author = package_author
        if not author and author_email:
            author = author_email
        if author and author_email and author_email not in author:
            author = f"{author} <{author_email}>"
        package.health_metadata.authors = author
    return package


def complete_package(package: Package) -> Package:
    pkg_advisories = advisories.get_package_advisories(package)
    if pkg_advisories:
        package.advisories = pkg_advisories
    current_package = get_pypi_package(package.name, package.version)
    pypi_package = get_pypi_package(package.name)
    if not pypi_package:
        return package
    try:
        package.health_metadata = HealthMetadata(
            latest_version=pypi_package["info"]["version"],
            latest_version_created_at=(
                pypi_package["releases"][pypi_package["info"]["version"]][0][
                    "upload_time_iso_8601"
                ]
            ),
        )
    except IndexError:
        return package
    package = _set_health_metadata_artifact(
        package=package, current_package=current_package
    )
    package = _set_authors(package=package, pypi_package=pypi_package)
    if not package.licenses and (
        licenses := pypi_package["info"].get("license")
    ):
        if isinstance(licenses, str):
            package.licenses = [licenses]
        else:
            raise UnexpectedValueType("license must be an string")
    return package
