from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class CocoaPodfileLockEntry:
    checksum: str
