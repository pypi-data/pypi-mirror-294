from fluid_sbom.file.location import (
    Location,
)
from fluid_sbom.linux.release import (
    Release,
)
from fluid_sbom.pkg.alpm import (
    AlpmDBEntry,
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
from fluid_sbom.pkg.url import (
    purl_qualifiers,
)
import logging
from packageurl import (
    PackageURL,
)
from pydantic import (
    ValidationError,
)

LOGGER = logging.getLogger(__name__)


def package_url(
    entry: AlpmDBEntry, distro: Release | None = None
) -> str | None:
    if not distro or distro.id_ != "arch":
        return None

    qualifiers = {"arch": entry.architecture}
    if entry.base_package:
        qualifiers["upstream"] = entry.base_package
    return PackageURL(
        type="almp",
        name=entry.package,
        version=entry.version,
        qualifiers=purl_qualifiers(qualifiers, distro),  # type: ignore
        namespace="",
        subpath="",
    ).to_string()


def new_package(
    entry: AlpmDBEntry, release: Release | None, db_location: Location
) -> Package | None:
    licenses_candidates = entry.licenses.split("\n")
    try:
        return Package(
            name=entry.package,
            version=entry.version,
            locations=[db_location],
            licenses=licenses_candidates,
            type=PackageType.AlpmPkg,
            metadata=entry,
            p_url=package_url(entry, release),
            language=Language.UNKNOWN_LANGUAGE,
        )
    except ValidationError as ex:
        LOGGER.warning(
            "Malformed package. Required fields are missing or data "
            "types are incorrect.",
            extra={
                "extra": {
                    "exception": ex.errors(include_url=False),
                    "location": db_location.path(),
                }
            },
        )
        return None
