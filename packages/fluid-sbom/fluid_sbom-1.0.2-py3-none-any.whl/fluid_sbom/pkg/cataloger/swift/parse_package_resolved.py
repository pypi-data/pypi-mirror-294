from copy import (
    deepcopy,
)
from fluid_sbom.artifact.relationship import (
    Relationship,
)
from fluid_sbom.file.location_read_closer import (
    LocationReadCloser,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.internal.collection.json import (
    parse_json_with_tree_sitter,
)
from fluid_sbom.internal.collection.types import (
    IndexedDict,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.cataloger.swift.package import (
    new_swift_package_manager_package,
)
from fluid_sbom.pkg.package import (
    Package,
)
import logging
from typing import (
    cast,
)

LOGGER = logging.getLogger(__name__)


def parse_package_resolved(
    _: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    try:
        package_resolved: IndexedDict = cast(
            IndexedDict, parse_json_with_tree_sitter(reader.read_closer.read())
        )
    except ValueError:
        LOGGER.warning(
            "Failed to parse package.json",
            extra={
                "extra": {
                    "location": reader.location,
                }
            },
        )
        return [], []
    packages: list[Package] = []
    relationships: list[Relationship] = []

    for pin in package_resolved["pins"]:
        name = pin["identity"]
        version = pin["state"]["version"]
        new_location = deepcopy(reader.location)
        if new_location.coordinates:
            new_location.coordinates.line = pin.position.start.line

        if pkg := new_swift_package_manager_package(
            name,
            version,
            pin["location"],
            pin["state"]["revision"],
            new_location,
        ):
            packages.append(pkg)

    return packages, relationships
