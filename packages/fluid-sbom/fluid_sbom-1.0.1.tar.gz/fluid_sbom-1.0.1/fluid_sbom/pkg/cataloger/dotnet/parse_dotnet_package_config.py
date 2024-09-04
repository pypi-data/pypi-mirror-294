from bs4 import (
    BeautifulSoup,
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

LOGGER = logging.getLogger(__name__)


def parse_dotnet_pkgs_config(
    _resolver: Resolver | None,
    _env: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    root = BeautifulSoup(reader.read_closer.read(), features="html.parser")
    packages = []

    for pkg in root.find_all("package", recursive=True):
        if (id_ := pkg.get("id")) and (version := pkg.get("version")):
            line = pkg.sourceline
            location = deepcopy(reader.location)
            if location.coordinates:
                location.coordinates.line = line
            try:
                packages.append(
                    Package(
                        name=id_,
                        version=version,
                        locations=[location],
                        language=Language.DOTNET,
                        licenses=[],
                        type=PackageType.DotnetPkg,
                        metadata=None,
                        p_url=PackageURL(
                            type="nuget",
                            namespace="",
                            name=id_,
                            version=version,
                            qualifiers={},
                            subpath="",
                        ).to_string(),
                    )
                )
            except ValidationError as ex:
                LOGGER.warning(
                    "Malformed package. Required fields are missing or data "
                    "types are incorrect.",
                    extra={
                        "extra": {
                            "exception": ex.errors(include_url=False),
                            "location": location.path(),
                        }
                    },
                )
                continue

    return packages, []
