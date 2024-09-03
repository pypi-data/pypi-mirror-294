from fluid_sbom.artifact.relationship import (
    Relationship,
)
from fluid_sbom.file.location_read_closer import (
    LocationReadCloser,
)
from fluid_sbom.file.resolver import (
    Resolver,
)
from fluid_sbom.pkg.cataloger.generic.parser import (
    Environment,
)
from fluid_sbom.pkg.cataloger.java.package import (
    package_url,
)
from fluid_sbom.pkg.java import (
    JavaArchive,
    JavaPomProperties,
)
from fluid_sbom.pkg.language import (
    Language,
)
from fluid_sbom.pkg.package import (
    Package,
)
from fluid_sbom.pkg.type import (
    PackageType,
)
import logging
import os
from pathlib import (
    Path,
)
from pydantic import (
    ValidationError,
)
import tempfile
import zipfile

LOGGER = logging.getLogger(__name__)


def parse_apk(
    _resolver: Resolver | None,
    _env: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    packages: list[Package] = []
    with tempfile.TemporaryDirectory() as output_folder:
        with zipfile.ZipFile(reader.read_closer.name, "r") as apk_file:
            apk_file.extractall(output_folder)
        files: list[str] = []
        meta_dir = os.path.join(output_folder, "META-INF")
        if os.path.exists(meta_dir):
            files = [
                os.path.join(meta_dir, file)
                for file in os.listdir(meta_dir)
                if file.endswith(".version")
            ]
        for file in files:
            with open(file, "r", encoding="utf-8") as version_reader:
                version = version_reader.read().strip()
            parts = Path(file).name.replace(".version", "").split("_", 1)
            group_id = parts[0]
            if not group_id:
                raise ValueError(
                    f"Invalid group_id for {file} in {reader.location}"
                )
            artifact_id = parts[1]
            java_archive = JavaArchive(
                pom_properties=JavaPomProperties(
                    group_id=group_id,
                    artifact_id=artifact_id,
                    version=version,
                )
            )
            try:
                packages.append(
                    Package(
                        name=artifact_id,
                        version=version,
                        licenses=[],
                        locations=[reader.location],
                        language=Language.JAVA,
                        type=PackageType.JavaPkg,
                        metadata=java_archive,
                        p_url=package_url(artifact_id, version, java_archive),
                    )
                )
            except ValidationError as ex:
                LOGGER.warning(
                    "Malformed package. Required fields are missing or data "
                    "types are incorrect.",
                    extra={
                        "extra": {
                            "exception": ex.errors(include_url=False),
                            "location": reader.location.path(),
                        }
                    },
                )
                continue
    return packages, []
