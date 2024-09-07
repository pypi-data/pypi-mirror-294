from fluid_sbom.internal.package_information.ruby import (
    get_gem_package,
)
from fluid_sbom.pkg.package import (
    Artifact,
    HealthMetadata,
    Package,
)
from fluid_sbom.utils.file import (
    Digest,
)
from packageurl import (
    PackageURL,
)


def package_url(name: str, version: str) -> str:
    return PackageURL(
        type="gem",
        namespace="",
        name=name,
        version=version,
        qualifiers=None,
        subpath="",
    ).to_string()


def complete_package(package: Package) -> Package:
    current_package = get_gem_package(package.name, package.version)
    gem_package = get_gem_package(package.name)
    if not gem_package:
        return package

    package.health_metadata = HealthMetadata(
        latest_version=gem_package["version"],
        latest_version_created_at=gem_package["version_created_at"],
    )
    if current_package:
        digest_value = gem_package.get("sha") or None
        package.health_metadata.artifact = Artifact(
            url=gem_package["gem_uri"],
            integrity=Digest(
                algorithm="sha" if digest_value else None,
                value=digest_value,
            ),
        )

    package.health_metadata.authors = gem_package["authors"]
    if not package.licenses and gem_package["licenses"]:
        package.licenses = gem_package["licenses"]
    return package
