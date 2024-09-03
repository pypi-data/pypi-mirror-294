from copy import (
    deepcopy,
)
from dataclasses import (
    dataclass,
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
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.cataloger.java.package import (
    package_url,
)
from fluid_sbom.pkg.java import (
    JavaArchive,
    JavaPomProject,
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
from pydantic import (
    ValidationError,
)

LOGGER = logging.getLogger(__name__)


@dataclass
class LockFileDependency:
    group: str
    name: str
    version: str
    line: int | None = None


def parse_gradle_lockfile(
    _resolver: Resolver | None,
    __: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    dependencies: list[LockFileDependency] = []
    packages: list[Package] = []
    for line_number, line in enumerate(reader.read_closer.readlines(), 1):
        if "=" in line and ":" in line:  # To ensure it's a dependency line
            dependency_part = line.split("=")[0]
            group, name, version = dependency_part.split(":")
            dependencies.append(
                LockFileDependency(group, name, version, line_number)
            )

    for dependency in dependencies:
        location = deepcopy(reader.location)
        if location.coordinates:
            location.coordinates.line = dependency.line

        archive = JavaArchive(
            pom_project=JavaPomProject(
                group_id=dependency.group,
                name=dependency.name,
                artifact_id=dependency.name,
                version=dependency.version,
            )
        )
        try:
            packages.append(
                Package(
                    name=dependency.name,
                    version=dependency.version,
                    locations=[location],
                    language=Language.JAVA,
                    type=PackageType.JavaPkg,
                    metadata=archive,
                    p_url=package_url(
                        dependency.name, dependency.version, archive
                    ),
                    licenses=[],
                )
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
            continue

    return packages, []
