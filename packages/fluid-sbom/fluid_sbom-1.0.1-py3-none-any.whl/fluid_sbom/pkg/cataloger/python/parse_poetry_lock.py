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
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.language import (
    Language,
)
from fluid_sbom.pkg.package import (
    Package,
)
from fluid_sbom.pkg.python import (
    PythonRequirementsEntry,
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
import tomlkit
from tomlkit.exceptions import (
    UnexpectedCharError,
)

LOGGER = logging.getLogger(__name__)


def find_dependency_line_numbers(
    _content: str, dependency_name: str
) -> int | None:
    return next(
        (
            line_number + 1
            for line_number, line in enumerate(_content.splitlines(), start=1)
            if f'name = "{dependency_name}"' in line
        ),
        None,
    )


def parse_poetry_lock(
    _resolver: Resolver, _env: Environment, reader: LocationReadCloser
) -> tuple[list[Package], list[Relationship]] | None:
    packages: list[Package] = []
    relationships: list[Relationship] = []
    _content = reader.read_closer.read()
    try:
        toml_content = tomlkit.parse(_content)
    except UnexpectedCharError:
        return [], []
    for package in toml_content.get("package", []):
        location = deepcopy(reader.location)
        if not location.coordinates:
            continue
        location.coordinates.line = find_dependency_line_numbers(
            _content, package["name"]
        )
        p_url = PackageURL(
            type="pypi",
            namespace="",
            name=package["name"],
            version=package["version"],
            qualifiers="",
            subpath="",
        ).to_string()
        try:
            packages.append(
                Package(
                    name=package["name"],
                    version=package["version"],
                    found_by=None,
                    locations=[location],
                    language=Language.PYTHON,
                    p_url=p_url,
                    metadata=PythonRequirementsEntry(
                        name=package["name"],
                        extras=[],
                        markers=p_url,
                    ),
                    licenses=[],
                    type=PackageType.PythonPkg,
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
    for package in toml_content.get("package", []):
        _pkg = next(
            (pkg for pkg in packages if pkg.name == package["name"]), None
        )
        dependencies: list[str] = list(package.get("dependencies", {}).keys())
        if _pkg and dependencies:
            pkg_dependencies = [
                pkg
                for dep in dependencies
                for pkg in packages
                if pkg.name == dep
            ]
            for dep in pkg_dependencies:
                relationships.append(
                    Relationship(
                        from_=dep,
                        to_=_pkg,
                        type=RelationshipType.DEPENDENCY_OF_RELATIONSHIP,
                        data=None,
                    )
                )

    return packages, relationships
