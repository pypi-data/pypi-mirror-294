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
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.cataloger.python.package import (
    package_url,
)
from fluid_sbom.pkg.language import (
    Language,
)
from fluid_sbom.pkg.package import (
    Package,
)
from fluid_sbom.pkg.python import (
    PythonPackage,
)
from fluid_sbom.pkg.type import (
    PackageType,
)
import logging
from pydantic import (
    ValidationError,
)
import tomlkit

LOGGER = logging.getLogger(__name__)


def _find_dependency_line_numbers(
    _content: str, dependency_name: str
) -> list[int]:
    lines = [
        line_number
        for line_number, line in enumerate(_content.splitlines(), start=1)
        if dependency_name in line
    ]
    return lines


def parse_pipfile_deps(
    _resolver: Resolver | None,
    _env: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    packages = []
    file_content = reader.read_closer.read()
    toml_content = tomlkit.parse(file_content)
    toml_packages = toml_content.get("packages", {})
    for package in toml_packages:
        version = toml_packages[package]
        if not isinstance(version, str):
            version = version.get("version", "*")
        if "*" in version:
            continue
        line = _find_dependency_line_numbers(file_content, package)
        location = deepcopy(reader.location)
        if location.coordinates:
            location.coordinates.line = line[0]

        version = version.strip("=<>~^ ")
        try:
            packages.append(
                Package(
                    name=package,
                    version=version,
                    locations=[location],
                    language=Language.PYTHON,
                    type=PackageType.PythonPkg,
                    metadata=PythonPackage(
                        name=package,
                        version=version,
                    ),
                    p_url=package_url(
                        name=package, version=version, package=None
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
