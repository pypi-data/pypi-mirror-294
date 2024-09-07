from fluid_sbom.internal.package_information.dotnet import (
    get_nuget_package,
)
from fluid_sbom.pkg.package import (
    Artifact,
    HealthMetadata,
    Package,
)
from fluid_sbom.utils.file import (
    Digest,
)
from typing import (
    Any,
)


def _set_health_metadata_artifact(
    package: Package,
    current_package: dict[str, Any] | None,
) -> Package:
    if current_package:
        # {LOWER_ID}/{LOWER_VERSION}/{LOWER_ID}.{LOWER_VERSION}.nupkg
        lower_id = current_package["id"].lower()
        lower_version = current_package["version"].lower()
        if package.health_metadata:
            digest_value = current_package.get("packageHash") or None
            algorithm = current_package.get("packageHashAlgorithm") or None
            package.health_metadata.artifact = Artifact(
                url=(
                    f"https://api.nuget.org/v3-flatcontainer/{lower_id}"
                    f"/{lower_version}/{lower_id}.{lower_version}.nupkg"
                ),
                integrity=Digest(
                    algorithm=algorithm if digest_value else None,
                    value=digest_value,
                ),
            )
    return package


def complete_package(package: Package) -> Package:
    current_package = get_nuget_package(package.name, package.version)
    nuget_package = get_nuget_package(package.name)
    if not nuget_package:
        return package
    try:
        package.health_metadata = HealthMetadata(
            latest_version=nuget_package["version"],
            latest_version_created_at=nuget_package["published"],
        )
    except IndexError:
        return package
    package = _set_health_metadata_artifact(package, current_package)
    if package.health_metadata:
        package.health_metadata.authors = nuget_package["authors"]
    if not package.licenses and nuget_package["licenseExpression"]:
        package.licenses = [nuget_package["licenseExpression"]]

    return package
