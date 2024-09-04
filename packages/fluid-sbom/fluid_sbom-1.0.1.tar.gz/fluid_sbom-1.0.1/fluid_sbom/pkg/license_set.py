from dataclasses import (
    dataclass,
)


@dataclass
class LicenseSet:
    set: dict[str, str]
