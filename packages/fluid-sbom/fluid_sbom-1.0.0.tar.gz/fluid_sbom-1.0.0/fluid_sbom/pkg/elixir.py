from dataclasses import (
    dataclass,
)


@dataclass
class ElixirMixLockEntry:
    name: str
    version: str
    pkg_hash: str
    pkg_hash_ext: str
