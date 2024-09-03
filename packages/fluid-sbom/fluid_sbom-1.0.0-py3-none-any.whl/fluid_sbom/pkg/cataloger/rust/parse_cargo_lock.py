from copy import (
    deepcopy,
)
from fluid_sbom.artifact.relationship import (
    Relationship,
    RelationshipType,
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
from fluid_sbom.internal.collection.toml import (
    parse_toml_with_tree_sitter,
)
from fluid_sbom.internal.collection.types import (
    UnexpectedNode,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.cataloger.rust.package import (
    package_url,
)
from fluid_sbom.pkg.language import (
    Language,
)
from fluid_sbom.pkg.package import (
    Package,
)
from fluid_sbom.pkg.rust import (
    RustCargoLockEntry,
)
from fluid_sbom.pkg.type import (
    PackageType,
)
import logging
from pydantic import (
    ValidationError,
)

LOGGER = logging.getLogger(__name__)


def _create_package(pkg: dict, location: Location) -> Package | None:
    current_location = deepcopy(location)
    if current_location.coordinates and hasattr(pkg, "position"):
        current_location.coordinates.line = pkg.position.start.line

    try:
        return Package(
            name=pkg["name"],
            version=pkg["version"],
            locations=[current_location],
            language=Language.RUST,
            licenses=[],
            p_url=package_url(pkg["name"], pkg["version"]),
            type=PackageType.RustPkg,
            metadata=RustCargoLockEntry(
                name=pkg["name"],
                version=pkg["version"],
                source=pkg.get("source"),
                dependencies=pkg.get("dependencies", []),
                checksum=pkg.get("checksum"),
            ),
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
        return None


def _create_relationships(packages: list[Package]) -> list[Relationship]:
    relationships = []
    for pkg in packages:
        if isinstance(pkg.metadata, RustCargoLockEntry):
            for dep_name in pkg.metadata.dependencies:
                if dep := next(
                    (x for x in packages if x.name == dep_name), None
                ):
                    relationships.append(
                        Relationship(
                            pkg,
                            dep,
                            RelationshipType.DEPENDENCY_OF_RELATIONSHIP,
                            None,
                        )
                    )
    return relationships


def parse_cargo_lock(
    _: Resolver | None, __: Environment | None, reader: LocationReadCloser
) -> tuple[list[Package], list[Relationship]]:
    packages: list[Package] = []

    if not reader.location.coordinates:
        return packages, []

    _content = reader.read_closer.read()
    try:
        toml = parse_toml_with_tree_sitter(_content)
    except UnexpectedNode:
        return [], []

    for pkg in toml.get("package", []):
        if package := _create_package(pkg, reader.location):
            packages.append(package)

    relationships = _create_relationships(packages)

    return packages, relationships
