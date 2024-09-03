from dataclasses import (
    dataclass,
)
from fluid_sbom.utils.file import (
    Digest,
)


@dataclass
class DpkgFileRecord:
    path: str
    digest: Digest | None = None
    is_config_file: bool | None = None


@dataclass
class DpkgDBEntry:  # pylint:disable=too-many-instance-attributes
    package: str
    source: str | None = None
    version: str | None = None
    source_version: str | None = None
    architecture: str | None = None
    maintainer: str | None = None
    installed_size: int | None = None
    description: str | None = None
    provides: list[str] | None = None
    dependencies: list[str] | None = None
    pre_dependencies: list[str] | None = None
    files: list[DpkgFileRecord] | None = None
