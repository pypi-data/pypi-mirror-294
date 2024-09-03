# pylint:disable=too-many-instance-attributes
from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class PythonFileDigest:
    algorithm: str
    value: str


@dataclass(frozen=True)
class PythonFileRecord:
    path: str
    digest: PythonFileDigest | None = None
    size: str | None = None


@dataclass(frozen=True)
class PythonDirectURLOriginInfo:
    url: str
    commit_id: str | None
    vcs: str | None


@dataclass
class PythonPackage:
    name: str
    version: str | None = None
    author: str | None = None
    author_email: str | None = None
    platform: str | None = None
    files: list[PythonFileRecord] | None = None
    site_package_root_path: str | None = None
    top_level_packages: list[str] | None = None
    direct_url_origin: PythonDirectURLOriginInfo | None = None
    dependencies: list[str] | None = None


@dataclass(frozen=True)
class PythonRequirementsEntry:
    name: str
    extras: list[str] | None
    markers: str | None
    version_constraint: str | None = None
