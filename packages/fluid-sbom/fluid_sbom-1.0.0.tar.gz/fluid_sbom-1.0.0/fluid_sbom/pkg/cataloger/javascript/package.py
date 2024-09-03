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
from fluid_sbom.internal.collection.types import (
    IndexedDict,
)
from fluid_sbom.internal.package_information.javascript import (
    get_npm_package,
    NPMPackage,
)
from fluid_sbom.pkg.language import (
    Language,
)
from fluid_sbom.pkg.npm import (
    NpmPackageLockEntry,
)
from fluid_sbom.pkg.package import (
    Artifact,
    HealthMetadata,
    Package,
)
from fluid_sbom.pkg.type import (
    PackageType,
)
from fluid_sbom.utils.file import (
    Digest,
)
from fluid_sbom.utils.package import (
    handle_licenses,
)
import logging
from packageurl import (
    PackageURL,
)
from pydantic import (
    ValidationError,
)

LOGGER = logging.getLogger(__name__)


def new_package_lock_v1(
    location: Location,
    name: str,
    value: IndexedDict,
) -> Package | None:
    version: str = value.get("version", "")
    alias_prefix_package_lock = "npm:"
    if version.startswith(alias_prefix_package_lock):
        name, version = version.removeprefix(alias_prefix_package_lock).split(
            "@"
        )
    current_location = deepcopy(location)
    if current_location.coordinates:
        current_location.coordinates.line = value.position.start.line
    try:
        return Package(
            name=name,
            version=version,
            locations=[current_location],
            language=Language.JAVASCRIPT,
            licenses=[],
            type=PackageType.NpmPkg,
            metadata=NpmPackageLockEntry(
                value["resolved"],
                integrity=value["integrity"],
                is_dev=value.get("dev", False),
            )
            if "resolved" in value and "integrity" in value
            else None,
            p_url=package_url(name, version),
        )
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data types "
            "are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),
                    "location": location.path(),
                }
            },
        )
        return None


def new_package_lock_v2(
    location: Location,
    name: str,
    value: IndexedDict,
) -> Package | None:
    version: str = value.get("version", "")
    current_location = location

    if not name or not version:
        return None

    if current_location.coordinates:
        current_location.coordinates.line = value.position.start.line

    try:
        return Package(
            name=name,
            version=version,
            locations=[current_location],
            language=Language.JAVASCRIPT,
            licenses=[],
            type=PackageType.NpmPkg,
            metadata=NpmPackageLockEntry(
                value.get("resolved"),
                integrity=value.get("integrity"),
                is_dev=value.get("dev", False),
            ),
            p_url=package_url(name, version),
        )
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data types "
            "are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),
                    "location": location.path(),
                }
            },
        )
        return None


def package_url(name: str, version: str) -> str:
    namespace = ""
    fields = name.split("/", 2)
    if len(fields) > 1:
        namespace = fields[0]
        name = fields[1]
    return PackageURL(
        type="npm",
        namespace=namespace,
        name=name,
        version=version,
        qualifiers={},
        subpath="",
    ).to_string()


def _set_author(npm_package: NPMPackage) -> str | None:
    author: str | None = None
    if "author" in npm_package:
        package_author = npm_package["author"]
        if isinstance(package_author, dict) and "name" in package_author:
            author = package_author["name"]
            if "email" in package_author:
                author = f'{author} <{package_author["email"]}>'
        elif package_author and isinstance(package_author, str):
            author = str(package_author)
        return author
    return None


def complete_package(package: Package) -> Package:
    pkg_advisories = advisories.get_package_advisories(package)
    if pkg_advisories:
        package.advisories = pkg_advisories

    npm_package = get_npm_package(package.name)
    if not npm_package:
        return package

    latest_version = None
    latest_version_created_at = None
    if npm_package.get("versions"):
        latest_version = list(npm_package["versions"].keys())[-1]
        latest_version_created_at = npm_package["time"]["modified"]

    current_package = npm_package["versions"].get(package.version)
    artifact = None
    if current_package:
        with suppress(KeyError):
            digest_value = (
                current_package.get("dist", {}).get("integrity") or None
            )
            artifact = Artifact(
                url=current_package["dist"]["tarball"],
                integrity=Digest(
                    algorithm="sha512" if digest_value else None,
                    value=digest_value,
                ),
            )

    package.health_metadata = HealthMetadata(
        latest_version=latest_version,
        latest_version_created_at=latest_version_created_at,
        artifact=artifact,
        authors=_set_author(npm_package),
    )

    licenses = npm_package.get("license") or None
    if licenses and isinstance(licenses, str | list | dict):
        package.licenses = handle_licenses(licenses)

    return package
