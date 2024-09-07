from copy import (
    deepcopy,
)
from fluid_sbom.artifact.relationship import (
    Relationship,
    RelationshipType,
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
from fluid_sbom.pkg.cataloger.javascript.package import (
    new_package_lock_v1,
    new_package_lock_v2,
)
from fluid_sbom.pkg.package import (
    Package,
)
import logging
from typing import (
    cast,
)

LOGGER = logging.getLogger(__name__)


def get_name_from_path(name: str) -> str:
    return name.split("node_modules/")[-1]


def handle_v1(
    reader: LocationReadCloser,
    package_json: IndexedDict,
) -> tuple[list[Package], list[Relationship]]:
    packages: list[Package] = []
    relationships: list[Relationship] = []

    deps = package_json.get("dependencies", {})
    for dependency_key, dependency_value in deps.items():
        name: str = dependency_key
        if pkg := new_package_lock_v1(
            reader.location,
            name,
            dependency_value,
        ):
            packages.append(pkg)

        requires = [
            package
            for package in packages
            if package.name in dependency_value.get("requires", {})
        ]
        current_package: Package | None = next(
            (
                package
                for package in packages
                if package.name == dependency_key
            ),
            None,
        )
        if not current_package:
            continue
        relationships.extend(
            [
                Relationship(
                    require,
                    current_package,
                    RelationshipType.DEPENDENCY_OF_RELATIONSHIP,
                    None,
                )
                for require in requires
            ]
        )

    return packages, relationships


def _get_name(dependency_key: str, package_value: IndexedDict) -> str | None:
    name = dependency_key
    if not name:
        if "name" not in package_value:
            return None
        name = package_value["name"]

    # handle alias name
    if "name" in package_value and package_value["name"] != dependency_key:
        name = package_value["name"]

    return get_name_from_path(name)


def handle_v2(
    reader: LocationReadCloser,
    package_json: IndexedDict,
) -> tuple[list[Package], list[Relationship]]:
    packages: list[Package] = []
    relationships: list[Relationship] = []
    pkgs = package_json.get("packages", {})

    for dependency_key, package_value in pkgs.items():
        if not dependency_key:
            continue
        name = _get_name(dependency_key, package_value)
        if pkg := (
            new_package_lock_v2(
                deepcopy(reader.location),
                get_name_from_path(name or dependency_key),
                package_value,
            )
        ):
            packages.append(pkg)

    for dependency_key, package_value in pkgs.items():
        name = name = _get_name(dependency_key, package_value)
        dependencies = [
            package
            for package in packages
            if package.name in package_value.get("dependencies", {})
        ]
        if not dependencies:
            continue
        current_package: Package | None = next(
            (package for package in packages if package.name == name), None
        )
        if not current_package:
            continue
        relationships.extend(
            [
                Relationship(
                    dependency,
                    current_package,
                    RelationshipType.DEPENDENCY_OF_RELATIONSHIP,
                    None,
                )
                for dependency in dependencies
            ]
        )

    return packages, relationships


def parse_package_lock(
    _resolver: Resolver | None,
    _environment: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    try:
        package_json: IndexedDict = cast(
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

    match package_json.get("lockfileVersion", 1):
        case 1:
            return handle_v1(reader, package_json)
        case 2 | 3:
            return handle_v2(reader, package_json)

    return packages, relationships
