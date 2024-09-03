from dataclasses import (
    dataclass,
)
from fluid_sbom.file.location import (
    Location,
)
from typing import (
    TextIO,
)


@dataclass
class LocationReadCloser:
    location: Location
    read_closer: TextIO
