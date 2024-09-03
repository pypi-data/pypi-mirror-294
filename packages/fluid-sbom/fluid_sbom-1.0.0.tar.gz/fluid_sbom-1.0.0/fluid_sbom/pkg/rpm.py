from dataclasses import (
    dataclass,
)
from fluid_sbom.utils.file import (
    Digest,
)


@dataclass
class RpmFileRecord:
    path: str
    mode: int
    size: int
    digest: Digest
    username: str
    group_name: str | None
    flags: str


@dataclass
class RpmDBEntry:  # pylint: disable=too-many-instance-attributes
    id_: str
    name: str
    version: str
    epoch: int | None
    arch: str
    release: str
    source_rpm: str
    size: int
    vendor: str
    modularitylabel: str
    files: list[RpmFileRecord]
