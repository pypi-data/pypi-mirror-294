from datetime import (
    datetime,
)
from fluid_sbom.internal.package_information.java import (
    get_maven_package_info,
    MavenPackageInfo,
    search_maven_package,
)
from fluid_sbom.pkg.java import (
    JavaArchive,
    JavaPomProject,
    JavaPomProperties,
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
from typing import (
    Any,
)


def looks_like_group_id(group_id: str) -> bool:
    return "." in group_id


def remove_osgi_directives(group_id: str) -> str:
    return group_id.split(";")[0]


def clean_group_id(group_id: str) -> str:
    return remove_osgi_directives(group_id).strip()


def group_id_from_pom_properties(
    properties: JavaPomProperties | None,
) -> str:
    if not properties:
        return ""
    if properties.group_id:
        return clean_group_id(properties.group_id)
    if properties.artifact_id and looks_like_group_id(properties.artifact_id):
        return clean_group_id(properties.artifact_id)

    return ""


def group_id_pom_project(project: JavaPomProject | None) -> str:
    if not project:
        return ""

    if project.group_id:
        return clean_group_id(project.group_id)

    if project.artifact_id and looks_like_group_id(project.artifact_id):
        return clean_group_id(project.artifact_id)

    if project.parent:
        if project.parent.group_id:
            return clean_group_id(project.parent.group_id)

        if looks_like_group_id(project.parent.artifact_id):
            return clean_group_id(project.parent.artifact_id)

    return ""


def group_id_from_java_metadata(_pkg_name: str, metadata: Any) -> str | None:
    if hasattr(metadata, "pom_properties") and (
        group_id := group_id_from_pom_properties(metadata.pom_properties)
    ):
        return group_id

    if hasattr(metadata, "pom_project") and (
        group_id := group_id_pom_project(metadata.pom_project)
    ):
        return group_id

    return None


def package_url(name: str, version: str, metadata: JavaArchive) -> str:
    group_id = name
    if (g_id := group_id_from_java_metadata(name, metadata)) and g_id:
        group_id = g_id
    return PackageURL(
        type="maven",
        namespace=group_id,
        name=name,
        version=version,
        qualifiers=None,
        subpath="",
    ).to_string()


def _set_health_metadata_artifact(
    package: Package,
    current_package: MavenPackageInfo | None,
) -> Package:
    if current_package and package.health_metadata and current_package.jar_url:
        digest_value = current_package.hash or None
        package.health_metadata.artifact = Artifact(
            url=current_package.jar_url,
            integrity=Digest(
                algorithm="sha1" if digest_value else None,
                value=digest_value,
            ),
        )
    return package


def _set_licenses(
    package: Package, maven_package: MavenPackageInfo
) -> Package:
    if not package.licenses:
        package.licenses = maven_package.licenses or []
    return package


def _set_authors(package: Package, maven_package: MavenPackageInfo) -> Package:
    if package.health_metadata and not package.health_metadata.authors:
        package.health_metadata.authors = ", ".join(
            maven_package.authors or []
        )
    return package


def complete_package(package: Package) -> Package:
    current_package: MavenPackageInfo | None = None
    group_id: str | None = None
    artifact_id: str = package.name
    version: str = package.version

    if g_id := group_id_from_java_metadata(package.name, package.metadata):
        group_id = g_id
    elif package_candidate := search_maven_package(
        package.name, package.version
    ):
        group_id = package_candidate.group

    if not group_id:
        return package

    maven_package = get_maven_package_info(group_id, package.name)
    if not maven_package and (
        package_candidate := search_maven_package(
            package.name, package.version
        )
    ):
        maven_package = get_maven_package_info(
            package_candidate.group, package.name
        )

    if not maven_package:
        return package
    if maven_package.latest_version and maven_package.release_date:
        try:
            package.health_metadata = HealthMetadata(
                latest_version=maven_package.latest_version,
                latest_version_created_at=datetime.fromtimestamp(
                    int(int(maven_package.release_date) / 1000)
                ),
            )
        except IndexError:
            return package
    if version and (
        current_package := get_maven_package_info(
            group_id,
            artifact_id,
            version,
        )
    ):
        package = _set_health_metadata_artifact(package, current_package)

    package = _set_authors(package, maven_package)
    package = _set_licenses(package, maven_package)

    return package
