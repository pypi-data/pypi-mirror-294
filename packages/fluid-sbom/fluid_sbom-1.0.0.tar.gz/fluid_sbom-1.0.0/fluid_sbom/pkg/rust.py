from dataclasses import (
    dataclass,
)


@dataclass
class RustCargoLockEntry:
    name: str
    version: str
    source: str | None
    checksum: str | None
    dependencies: list[str]
