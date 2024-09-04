from dataclasses import (
    dataclass,
)
from fluid_sbom.utils.file import (
    Digest,
)


@dataclass
class ApkFileRecord:
    path: str
    owner_uid: str | None = None
    owner_gid: str | None = None
    permissions: str | None = None
    digest: Digest | None = None


@dataclass
class ApkDBEntry:  # pylint: disable=too-many-instance-attributes
    package: str
    origin_package: str | None
    maintainer: str | None
    version: str
    architecture: str | None
    url: str | None
    description: str | None
    size: str
    installed_size: str | None
    dependencies: list[str]
    provides: list[str]
    checksum: str
    git_commit: str | None
    files: list[ApkFileRecord]
