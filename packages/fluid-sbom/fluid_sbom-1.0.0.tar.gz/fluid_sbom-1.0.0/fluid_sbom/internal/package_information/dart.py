from fluid_sbom.internal.package_information.api_interface import (
    make_get,
)
from typing import (
    Any,
)


def get_pub_package(
    package_name: str, version: str | None = None
) -> dict[str, Any] | None:
    if version:
        url = f"https://pub.dev/api/packages/{package_name}/versions/{version}"
    else:
        url = f"https://pub.dev/api/packages/{package_name}"

    package_info = make_get(url, timeout=20, headers={"Accept": "gzip"})
    return package_info
