from copy import (
    deepcopy,
)
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.internal.collection.types import (
    IndexedDict,
)
from fluid_sbom.internal.package_information.php import (
    get_composer_package,
)
from fluid_sbom.pkg.language import (
    Language,
)
from fluid_sbom.pkg.package import (
    Artifact,
    HealthMetadata,
    Package,
)
from fluid_sbom.pkg.php import (
    PhpComposerAuthors,
    PhpComposerExternalReference,
    PhpComposerInstalledEntry,
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


def package_url(name: str, version: str) -> str | None:
    pkg_name = ""
    vendor = ""
    fields = name.split("/")

    if len(fields) == 0:
        return ""

    if len(fields) == 1:
        pkg_name = name
    elif len(fields) == 2:
        vendor = fields[0]
        pkg_name = fields[1]
    else:
        vendor = fields[0]
        pkg_name = "-".join(fields[1:])

    purl = PackageURL(
        type="composer",
        namespace=vendor,
        name=pkg_name,
        version=version,
        qualifiers=None,
        subpath="",
    )

    return purl.to_string()


def new_package_from_composer(
    package: IndexedDict, location: Location, is_dev: bool = False
) -> Package | None:
    new_location = deepcopy(location)
    if new_location.coordinates:
        new_location.coordinates.line = package.position.start.line

    try:
        return Package(
            name=package["name"],
            version=package["version"],
            locations=[new_location],
            language=Language.PHP,
            licenses=list(package.get("license", [])),
            type=PackageType.PhpComposerPkg,
            p_url=package_url(package["name"], package["version"]),
            metadata=PhpComposerInstalledEntry(
                name=package["name"],
                version=package["version"],
                source=PhpComposerExternalReference(
                    package["source"]["type"],
                    package["source"]["url"],
                    package["source"]["reference"],
                    package["source"].get("shasum") or None,
                ),
                dist=PhpComposerExternalReference(
                    package["dist"]["type"],
                    package["dist"]["url"],
                    package["dist"]["reference"],
                    package["dist"].get("shasum") or None,
                ),
                require=package.get("require"),
                provide=package.get("provide"),
                require_dev=package.get("require-dev"),
                suggest=package.get("suggest"),
                license=package.get("license", []),
                type=package["type"],
                notification_url=package.get("notification-url"),
                bin=package.get("bin", []),
                authors=[
                    PhpComposerAuthors(
                        name=x["name"],
                        email=x.get("email"),
                        homepage=x.get("homepage"),
                    )
                    for x in package.get("authors", [])
                ],
                description=package.get("description"),
                homepage=package.get("homepage"),
                keywords=package.get("keywords", []),
                time=package.get("time"),
            ),
            is_dev=is_dev,
        )
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data types "
            "are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),
                    "location": new_location.path(),
                }
            },
        )
        return None


def package_url_from_pecl(pkg_name: str, version: str) -> str:
    purl = PackageURL(
        type="pecl",
        namespace="",
        name=pkg_name,
        version=version,
        qualifiers=None,
        subpath="",
    )
    return purl.to_string()


def _set_author(package: Package, composer_package: dict[str, Any]) -> Package:
    if not composer_package["authors"]:
        return package
    authors = []
    for author_item in composer_package["authors"]:
        author = author_item["name"]
        if "email" in author_item:
            author += f" <{author_item['email']}>"
        authors.append(author)
    if package.health_metadata and not package.health_metadata.authors:
        package.health_metadata.authors = ", ".join(authors)
    return package


def complete_package(package: Package) -> Package:
    current_package = get_composer_package(package.name, package.version)
    composer_package = get_composer_package(package.name)
    if not composer_package:
        return package

    package.health_metadata = HealthMetadata(
        latest_version=composer_package["version"],
        latest_version_created_at=composer_package["time"],
    )

    if not package.licenses:
        package.licenses = composer_package["license"]

    if current_package:
        digest_value = current_package.get("dist", {}).get("shasum") or None
        package.health_metadata.artifact = Artifact(
            url=current_package["dist"]["url"],
            integrity=Digest(
                algorithm="sha" if digest_value else None,
                value=digest_value,
            ),
        )
    package = _set_author(package, composer_package)

    return package
