from copy import (
    deepcopy,
)
from fluid_sbom.artifact.relationship import (
    Relationship,
)
from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.file.location_read_closer import (
    LocationReadCloser,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.internal.collection.types import (
    IndexedDict,
    Position,
)
from fluid_sbom.internal.collection.yaml import (
    parse_yaml_with_tree_sitter,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.dart import (
    DartPubspecLickEntry,
)
from fluid_sbom.pkg.language import (
    Language,
)
from fluid_sbom.pkg.package import (
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
from typing import (
    Any,
    cast,
)
from urllib3.util import (
    parse_url,
)

LOGGER = logging.getLogger(__name__)


def get_hosted_url(entry: dict[str, Any]) -> str:
    if (
        entry.get("hosted") == "hosted"
        and entry.get("description", {"url": "https://pub.dartlang.org"})[
            "url"
        ]
        != "https://pub.dartlang.org"
    ):
        if host := parse_url(entry["description"]["url"]).host:
            return host

        return entry["description"]["url"]

    return ""


def get_vcs_url(entry: dict[str, Any]) -> str:
    if entry.get("source") == "git":
        if entry.get("description", {}).get("path") == ".":
            return (
                entry["description"]["url"]
                + f'@{entry["description"]["resolved-ref"]}'
            )
        return (
            entry["description"]["url"]
            + f'@{entry["description"]["resolved-ref"]}'
            + f'#{entry["description"]["path"]}'
        )
    return ""


def package_url(entry: DartPubspecLickEntry) -> str:
    qualifiers = {}
    if entry.hosted_url:
        qualifiers["hosted_url"] = entry.hosted_url
    elif entry.vcs_url:
        qualifiers["vcs_url"] = entry.vcs_url

    return PackageURL(
        type="pub",
        namespace="",
        name=entry.name,
        version=entry.version,
        qualifiers=qualifiers,
        subpath="",
    ).to_string()


def parse_pubspec_lock(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    package_yaml: IndexedDict = cast(
        IndexedDict, parse_yaml_with_tree_sitter(reader.read_closer.read())
    )
    packages: list[Package] = []
    relationships: list[Relationship] = []
    for package_name, package_value in package_yaml["packages"].items():
        package_version = package_value["version"]
        current_location: Location = deepcopy(reader.location)
        if current_location.coordinates:
            position: Position = package_yaml["packages"].get_key_position(
                package_name
            )
            current_location.coordinates.line = position.start.line
        metadata = DartPubspecLickEntry(
            name=package_name,
            version=package_version,
            hosted_url=get_hosted_url(package_value),
            vcs_url=get_vcs_url(package_value),
        )
        try:
            packages.append(
                Package(
                    name=package_name,
                    version=package_version,
                    locations=[current_location],
                    language=Language.DART,
                    licenses=[],
                    type=PackageType.DartPubPkg,
                    p_url=package_url(metadata),
                    metadata=metadata,
                )
            )
        except ValidationError as ex:
            LOGGER.warning(
                "Malformed package. Required fields are missing or data types "
                "are incorrect.",
                extra={
                    "extra": {
                        "exception": ex.errors(include_url=False),
                        "location": current_location.path(),
                    }
                },
            )
            continue

    return packages, relationships
