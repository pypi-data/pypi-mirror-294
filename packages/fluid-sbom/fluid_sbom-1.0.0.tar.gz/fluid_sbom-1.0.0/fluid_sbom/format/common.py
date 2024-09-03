from dataclasses import (
    asdict,
    is_dataclass,
)
from fluid_sbom.config.config import (
    SbomConfig,
    SourceType,
)
from fluid_sbom.internal.file_resolver.container_image import (
    ContainerImage,
)
from fluid_sbom.internal.file_resolver.directory import (
    Directory,
)
from fluid_sbom.pkg.package import (
    Package,
)
from typing import (
    Any,
)


def _filter_none(item: dict | None) -> dict | None:
    """Recursively filter out None values, empty strings, and other empty
    collections from the dictionary."""
    if not isinstance(item, dict):
        return item

    def is_empty(value: Any) -> bool:
        """Check if a value is considered empty."""
        if value is None:
            return True
        if isinstance(value, str) and not value.strip():
            return True
        if isinstance(value, (list, dict)) and not value:
            return True
        return False

    return {k: _filter_none(v) for k, v in item.items() if not is_empty(v)}


def to_dict(obj: Any) -> dict | None:
    if obj is None:
        return None
    if not is_dataclass(obj):
        raise ValueError(
            "to_dict() should be called on dataclass instances only."
        )
    object_as_dict = asdict(obj)
    return object_as_dict if object_as_dict else None


def merge_packages(packages: list[Package]) -> list[Package]:
    merged_packages: dict = {}

    for package in packages:
        if package.id_:
            if package.id_ in merged_packages:
                merged_packages[package.id_].locations.extend(
                    x
                    for x in package.locations
                    if x not in merged_packages[package.id_].locations
                )
            else:
                merged_packages[package.id_] = package
        else:
            merged_packages[package] = package

    return list(merged_packages.values())


def process_packages(packages: list[Package]) -> list[Package]:
    packages = merge_packages(packages)
    return packages


def set_namespace_version(config: SbomConfig) -> tuple[str, str | None]:
    namespace = ""
    version = None
    if config.source_type == SourceType.DIRECTORY and isinstance(
        config.resolver, Directory
    ):
        namespace = config.resolver.root
    if config.source_type == SourceType.DOCKER and isinstance(
        config.resolver, ContainerImage
    ):
        namespace = config.resolver.context.image_ref
        version = config.resolver.context.id
    return namespace, version
