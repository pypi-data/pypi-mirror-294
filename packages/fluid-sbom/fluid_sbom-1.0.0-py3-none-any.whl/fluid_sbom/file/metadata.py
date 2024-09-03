from dataclasses import (
    dataclass,
)
from fluid_sbom.file.type import (
    Type,
)


@dataclass
class Metadata:
    path: str
    link_destination: str
    user_id: int
    group_id: int
    type: Type
    mime_type: str
