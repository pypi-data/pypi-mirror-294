from fluid_sbom.internal.package_information.dart import (
    get_pub_package,
)
from fluid_sbom.pkg.package import (
    Artifact,
    HealthMetadata,
    Package,
)
from fluid_sbom.utils.file import (
    Digest,
)


def complete_package(package: Package) -> Package:
    pub_package = get_pub_package(package.name)
    if not pub_package:
        return package

    current_package = get_pub_package(package.name, package.version)
    package.health_metadata = HealthMetadata(
        latest_version=pub_package["latest"]["version"],
        latest_version_created_at=pub_package["latest"]["published"],
    )
    if current_package:
        digest_value = (
            pub_package.get("latest", {}).get("archive_sha256") or None
        )
        package.health_metadata.artifact = Artifact(
            url=pub_package["latest"]["archive_url"],
            integrity=Digest(
                value=digest_value,
                algorithm="sha256" if digest_value else None,
            ),
        )

    package.health_metadata.authors = next(
        (
            x["pubspec"]["author"]
            for x in reversed(pub_package["versions"])
            if "author" in x["pubspec"]
        ),
        None,
    )

    return package
