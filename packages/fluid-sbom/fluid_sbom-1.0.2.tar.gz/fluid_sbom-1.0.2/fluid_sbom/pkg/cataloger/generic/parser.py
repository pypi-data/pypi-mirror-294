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
from fluid_sbom.linux.release import (
    Release,
)
from fluid_sbom.pkg.package import (
    Package,
)
from typing import (
    Callable,
)


@dataclass(frozen=True)
class Environment:
    linux_release: Release | None


Parser = Callable[
    [Resolver, Environment, LocationReadCloser],
    tuple[list[Package], list[Relationship]] | None,
]
