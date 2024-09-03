from fluid_sbom.internal.cache import (
    dual_cache,
)
import requests
from typing import (
    NotRequired,
    TypedDict,
)


class NPMPackageAuthor(TypedDict):
    email: str
    name: str


class NPMPackageDist(TypedDict):
    integrity: str
    tarball: str


class NPMPackageLicense(TypedDict):
    type: str
    url: str


class NPMPackageVersion(TypedDict):
    dist: NPMPackageDist
    name: str


class NPMPackageTimeUnpublished(TypedDict):
    time: str
    versions: list[str]


class NPMPackageTime(TypedDict):
    created: str
    modified: str
    unpublished: NotRequired[NPMPackageTimeUnpublished]


class NPMPackage(TypedDict):
    author: NotRequired[str | NPMPackageAuthor]
    license: str | NPMPackageLicense
    name: str
    time: NPMPackageTime
    versions: dict[str, NPMPackageVersion]


@dual_cache
def get_npm_package(package_name: str) -> NPMPackage | None:
    response = requests.get(
        f"https://registry.npmjs.org/{package_name}",
        timeout=20,
    )
    if response.status_code != 200:
        return None

    package: NPMPackage = response.json()
    if "unpublished" in package["time"]:
        return None
    return package
