from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class SwiftPackageManagerResolvedEntry:
    revision: str
