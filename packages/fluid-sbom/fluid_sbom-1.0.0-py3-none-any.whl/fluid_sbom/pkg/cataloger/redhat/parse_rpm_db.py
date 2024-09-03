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
from fluid_sbom.pkg.cataloger.redhat.package import (
    package_url,
)
from fluid_sbom.pkg.cataloger.redhat.parse_binary_info import (
    get_package_info,
    header_import,
    PackageInfo,
)
from fluid_sbom.pkg.language import (
    Language,
)
from fluid_sbom.pkg.package import (
    Package,
)
from fluid_sbom.pkg.rpm import (
    RpmDBEntry,
    RpmFileRecord,
)
from fluid_sbom.pkg.type import (
    PackageType,
)
from fluid_sbom.utils.file import (
    Digest,
)
from itertools import (
    zip_longest,
)
import logging
import os
from pydantic import (
    ValidationError,
)
import sqlite3

LOGGER = logging.getLogger(__name__)


def to_int(value: int | None, default: int = 0) -> int:
    return int(value) if isinstance(value, int) else default


def extract_rmp_file_records(
    resolver: Resolver, entry: PackageInfo
) -> list[RpmFileRecord]:
    records: list[RpmFileRecord] = []
    file_attributes = zip_longest(
        entry.base_names,
        entry.dir_indexes,
        entry.file_digests,
        entry.file_flags,
        entry.file_modes,
        entry.file_sizes,
        entry.user_names,
        entry.group_names,
    )

    for attrs in file_attributes:
        if record := create_rpm_file_record(resolver, entry, attrs):
            records.append(record)

    return records


def create_rpm_file_record(
    resolver: Resolver, entry: PackageInfo, attrs: tuple
) -> RpmFileRecord | None:
    (
        base_name,
        dir_index,
        file_digest,
        file_flag,
        file_mode,
        file_size,
        file_username,
        file_groupname,
    ) = attrs

    if not base_name or not isinstance(dir_index, int):
        return None

    file_path = os.path.join(str(entry.dir_names[dir_index]), str(base_name))
    file_location = resolver.files_by_path(file_path)

    if not file_location:
        return None

    return RpmFileRecord(
        path=file_path,
        mode=to_int(file_mode, default=0),
        size=to_int(file_size, default=0),
        digest=Digest(
            algorithm="md5" if file_digest else None, value=str(file_digest)
        ),
        username=str(file_username),
        flags=str(file_flag),
        group_name=str(file_groupname) if file_groupname else None,
    )


def parse_rpm_db(
    resolver: Resolver, env: Environment, reader: LocationReadCloser
) -> tuple[list[Package], list[Relationship]]:
    packages: list[Package] = []

    if not reader.location.coordinates:
        return packages, []

    connection = sqlite3.connect(reader.location.coordinates.real_path)
    cursor = connection.cursor()
    try:
        package_names = cursor.execute("SELECT * FROM Packages;").fetchall()
    except sqlite3.DatabaseError:
        return packages, []

    for item in package_names:
        index_ = header_import(item[1])
        entry = get_package_info(
            index_,
        )
        metadata = RpmDBEntry(
            id_="",
            name=entry.name,
            version=entry.version,
            epoch=entry.epoch,
            arch=entry.arch,
            release=entry.release,
            source_rpm=entry.source_rpm,
            vendor=entry.vendor,
            size=entry.size,
            modularitylabel=entry.modularitylabel,
            files=extract_rmp_file_records(resolver, entry),
        )
        try:
            packages.append(
                Package(
                    name=entry.name,
                    version=entry.version,
                    locations=[reader.location],
                    language=Language.UNKNOWN_LANGUAGE,
                    licenses=[entry.license],
                    type=PackageType.RpmPkg,
                    metadata=metadata,
                    p_url=package_url(
                        name=entry.name,
                        arch=entry.arch,
                        epoch=entry.epoch,
                        source_rpm=entry.source_rpm,
                        version=entry.version,
                        release=entry.release,
                        distro=env.linux_release,
                    ),
                )
            )
        except ValidationError as ex:
            LOGGER.warning(
                "Malformed package. Required fields are missing or data types "
                "are incorrect.",
                extra={
                    "extra": {
                        "exception": ex.errors(include_url=False),
                        "location": reader.location.path(),
                    }
                },
            )
            continue

    return packages, []
