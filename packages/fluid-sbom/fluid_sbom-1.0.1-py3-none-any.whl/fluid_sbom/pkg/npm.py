from dataclasses import (
    dataclass,
)
from fluid_sbom.utils.file import (
    Digest,
)


@dataclass
class NpmPackage:  # pylint:disable=too-many-instance-attributes
    name: str
    version: str | None = None
    author: str | None = None
    homepage: str | None = None
    description: str | None = None
    url: str | None = None
    private: bool | None = None
    is_dev: bool = False


@dataclass
class NpmPackageLockEntry:
    resolved: str | None = None
    integrity: str | None = None
    is_dev: bool = False


@dataclass
class YarnLockEntry:
    resolved: str | None = None
    integrity: str | None = None


@dataclass
class PnpmEntry:
    is_dev: bool = False
    integrity: Digest | None = None
