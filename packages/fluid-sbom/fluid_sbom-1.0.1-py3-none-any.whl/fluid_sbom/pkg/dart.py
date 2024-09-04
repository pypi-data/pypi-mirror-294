from dataclasses import (
    dataclass,
)


@dataclass
class DartPubspecLickEntry:
    name: str
    version: str
    hosted_url: str
    vcs_url: str
