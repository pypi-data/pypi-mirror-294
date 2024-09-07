from contextlib import (
    suppress,
)
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
import requirements
from requirements.requirement import (
    Requirement,
)

LOGGER = logging.getLogger(__name__)


def get_dep_version_range(dep_specs: list[tuple[str, str]]) -> str:
    version_range = ""
    for operator, version in dep_specs:
        if operator in {"==", "~="}:
            version_range = version
            break
        version_range += f"{operator}{version} "
    return version_range.rstrip()


def get_parsed_dependency(line: str) -> tuple[str, str, Requirement] | None:
    with suppress(Exception):
        parsed_dep = list(requirements.parse(line))[0]

        if not parsed_dep.specs:
            return None

        version = get_dep_version_range(parsed_dep.specs)
        return str(parsed_dep.name), version, parsed_dep
    return None


def parse_requirements_txt(
    _resolver: Resolver, _env: Environment, reader: LocationReadCloser
) -> tuple[list[Package], list[Relationship]] | None:
    deps_found = False
    packages: list[Package] = []
    file_lines = []
    with suppress(UnicodeDecodeError):
        file_lines = reader.read_closer.read().splitlines()

    for line_number, line in enumerate(file_lines, 1):
        parsed_dep = get_parsed_dependency(line)

        # Avoid parsing big txt files that have nothing to do with pip
        if not parsed_dep and not deps_found and line_number > 3:
            return None

        if not parsed_dep:
            continue
        product, version, req = parsed_dep

        p_url = PackageURL(
            type="pypi",
            namespace="",
            name=product,
            version=version,
            qualifiers="",
            subpath="",
        ).to_string()
        current_location = deepcopy(reader.location)
        if current_location.coordinates:
            current_location.coordinates.line = line_number

        try:
            packages.append(
                Package(
                    name=product,
                    version=version,
                    found_by=None,
                    locations=[current_location],
                    language=Language.PYTHON,
                    p_url=p_url,
                    metadata=PythonRequirementsEntry(
                        name=str(req.name),
                        extras=req.extras,
                        version_constraint=",".join(req.specs[0])
                        if req.specs
                        else "",
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
                        "location": current_location.path(),
                    }
                },
            )
            continue
    return packages, []
