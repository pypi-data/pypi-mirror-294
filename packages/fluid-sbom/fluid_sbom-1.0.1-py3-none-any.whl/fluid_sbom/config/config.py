from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from typing import (
    Type,
)


class SourceType(Enum):
    DIRECTORY = "dir"
    DOCKER = "docker"
    DOCKER_DAEMON = "docker-daemon"

    @classmethod
    def from_string(cls: Type["SourceType"], value: str) -> "SourceType":
        for member in cls:
            if member.value == value.lower():
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")


@dataclass
class SbomConfig:
    source: str
    source_type: SourceType
    output_format: str
    output: str
    resolver: Resolver | None = None
