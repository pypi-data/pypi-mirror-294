from fluid_sbom.internal.cache import (
    dual_cache,
)
import requests
from typing import (
    Any,
)


@dual_cache
def get_composer_package(
    package_name: str, version: str | None = None
) -> dict[str, Any] | None:
    base_url = f"https://repo.packagist.org/p2/{package_name}.json"
    response = requests.get(base_url, timeout=20)
    if response.status_code == 200:
        package_data = response.json()
        if version:
            # Search for the specific version in the package data
            for package_version in package_data["packages"][package_name]:
                if package_version["version"] == version:
                    return package_version
            return None  # Version not found

        latest_version = package_data["packages"][package_name][0]
        return latest_version

    return None
