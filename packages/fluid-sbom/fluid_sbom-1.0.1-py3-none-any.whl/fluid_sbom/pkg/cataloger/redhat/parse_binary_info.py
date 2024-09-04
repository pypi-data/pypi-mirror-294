# This package is a small adaptation of
# https://github.com/knqyf263/go-rpmdb/tree/master
# There was no package for python that allowed interacting with the rpm db
from dataclasses import (
    dataclass,
    field,
)
import struct

RPMTAG_HEADERIMAGE = 61
RPMTAG_HEADERSIGNATURES = 62
RPMTAG_HEADERIMMUTABLE = 63
HEADER_I18NTABLE = 100
RPMTAG_HEADERI18NTABLE = HEADER_I18NTABLE

# // rpmTag_e
# // ref. https://github.com/rpm-software-management/rpm/blob
# /061ba962297eba71ecb1b45a4133cbbd86f8450e/lib/rpmtag.h#L34
RPMTAG_SIGMD5 = 261  # x
RPMTAG_NAME = 1000  # s
RPMTAG_VERSION = 1001  # s
RPMTAG_RELEASE = 1002  # s
RPMTAG_EPOCH = 1003  # i
RPMTAG_INSTALLTIME = 1008  # i
RPMTAG_SIZE = 1009  # i
RPMTAG_VENDOR = 1011  # s
RPMTAG_LICENSE = 1014  # s
RPMTAG_ARCH = 1022  # s */
RPMTAG_FILESIZES = 1028  # i[]
# ref https://github.com/rpm-software-management/rpm/blob
# /2153fa4ae51a84547129b8ebb3bb396e1737020e/lib/rpmtypes.h#L53
RPMTAG_FILEMODES = 1030  # h[] , specifically []uint16
RPMTAG_FILEDIGESTS = 1035  # s[]
RPMTAG_FILEFLAGS = 1037  # i[]
RPMTAG_FILEUSERNAME = 1039  # s[]
RPMTAG_FILEGROUPNAME = 1040  # s[]
RPMTAG_SOURCERPM = 1044  # s
RPMTAG_PROVIDENAME = 1047  # s[]
RPMTAG_REQUIRENAME = 1049  # s[]
RPMTAG_DIRINDEXES = 1116  # i[]
RPMTAG_BASENAMES = 1117  # s[]
RPMTAG_DIRNAMES = 1118  # s[]
RPMTAG_FILEDIGESTALGO = 5011  # i
RPMTAG_SUMMARY = 1004  # s
RPMTAG_PGP = 259  # b
# rpmTag_enhances
# https://github.com/rpm-software-management/rpm/blob
# /rpm-4.16.0-release/lib/rpmtag.h#L375
RPMTAG_MODULARITYLABEL = 5096

# rpmTagType_e
# ref. https://github.com/rpm-software-management/rpm/blob
# /rpm-4.14.3-release/lib/rpmtag.h#L431
RPM_MIN_TYPE = 0
RPM_NULL_TYPE = 0
RPM_CHAR_TYPE = 1
RPM_INT8_TYPE = 2
RPM_INT16_TYPE = 3
RPM_INT32_TYPE = 4
RPM_INT64_TYPE = 5
RPM_STRING_TYPE = 6
RPM_BIN_TYPE = 7
RPM_STRING_ARRAY_TYPE = 8
RPM_I18NSTRING_TYPE = 9
RPM_MAX_TYPE = 9


ENTRY_INFO_SIZE = struct.calcsize(
    "iIii"
)  # size of entryInfo using struct format (int32, uint32, int32, uint32)

REGION_TAG_TYPE = RPM_BIN_TYPE
REGION_TAG_COUNT = ENTRY_INFO_SIZE


# Constants as per the Go code
HEADER_MAX_BYTES = 256 * 1024 * 1024
TYPE_SIZES = [
    0,  # RPM_NULL_TYPE
    1,  # RPM_CHAR_TYPE
    1,  # RPM_INT8_TYPE
    2,  # RPM_INT16_TYPE
    4,  # RPM_INT32_TYPE
    8,  # RPM_INT64_TYPE
    -1,  # RPM_STRING_TYPE
    1,  # RPM_BIN_TYPE
    -1,  # RPM_STRING_ARRAY_TYPE
    -1,  # RPM_I18NSTRING_TYPE
    0,  # Undefined, replace or extend these as necessary
    0,
    0,
    0,
    0,
    0,
]

TYPE_ALIGN = [
    1,  # RPM_NULL_TYPE
    1,  # RPM_CHAR_TYPE
    1,  # RPM_INT8_TYPE
    2,  # RPM_INT16_TYPE
    4,  # RPM_INT32_TYPE
    8,  # RPM_INT64_TYPE
    1,  # RPM_STRING_TYPE
    1,  # RPM_BIN_TYPE
    1,  # RPM_STRING_ARRAY_TYPE
    1,  # RPM_I18NSTRING_TYPE
    0,  # Undefined, replace or extend these as necessary
    0,
    0,
    0,
    0,
    0,
]


@dataclass
class EntryInfo:
    tag: int  # int32
    type_: int  # uint32
    offset: int  # int32
    count: int  # uint32


@dataclass
class HdrBlob:  # pylint: disable=too-many-instance-attributes
    package_entry_list: list[EntryInfo]
    idle_length: int  # int32
    data_length: int  # int32
    package_value_length: int  # int32
    data_start: int
    data_end: int
    region_tag: int
    ril: int
    rdl: int


@dataclass
class IndexEntry:
    info: EntryInfo
    length: int
    rdlen: int
    data: bytes


@dataclass
class PackageInfo:  # pylint: disable=too-many-instance-attributes
    epoch: int | None = None
    name: str = ""
    version: str = ""
    release: str = ""
    arch: str = ""
    source_rpm: str = ""
    size: int = 0
    license: str = ""
    vendor: str = ""
    modularitylabel: str = ""
    summary: str = ""
    pgp: str = ""
    sig_md5: str = ""
    digest_algorithm: str = ""
    install_time: int = 0
    base_names: list[str] = field(default_factory=list)
    dir_indexes: list[int] = field(default_factory=list)
    dir_names: list[str] = field(default_factory=list)
    file_sizes: list[int] = field(default_factory=list)
    file_digests: list[str] = field(default_factory=list)
    file_modes: list[int] = field(default_factory=list)
    file_flags: list[int] = field(default_factory=list)
    user_names: list[str] = field(default_factory=list)
    group_names: list[str] = field(default_factory=list)
    provides: list[str] = field(default_factory=list)
    requires: list[str] = field(default_factory=list)


@dataclass
class FileInfo:
    path: str = ""
    mode: int = 0
    digest: str = ""
    size: int = 0
    username: str = ""
    groupname: str = ""
    flags: int = 0


def parse_int32_array(data: bytes) -> list[int]:
    format_str = f">{len(data) // 4}i"  # Big-endian int32
    return list(struct.unpack(format_str, data))


def parse_string_array(data: bytes) -> list[str]:
    if data.endswith(b"\x00"):
        data = data[:-1]
    return data.decode("utf-8").lstrip("\x00").split("\x00")


def parse_int32(data: bytes) -> int:
    return struct.unpack(">i", data)[0]  # Big-endian int32


def uint16_array(data: bytes) -> list[int]:
    format_str = f">{len(data) // 2}H"  # Big-endian uint16
    return list(struct.unpack(format_str, data))


def hdrblob_init(data: bytes) -> HdrBlob:
    try:
        # Read il and dl using BigEndian
        idle_length, data_length_ = struct.unpack(">ii", data[:8])
        data_start = 8 + idle_length * ENTRY_INFO_SIZE
        package_value_length = 8 + idle_length * ENTRY_INFO_SIZE + data_length_
        data_end = data_start + data_length_

        if idle_length < 1:
            raise ValueError("Region no tags error")

        package_entry_list = []
        offset = 8
        for _ in range(idle_length):
            # Read each entryInfo using LittleEndian
            if offset + ENTRY_INFO_SIZE > len(data):
                raise ValueError("Data out of bounds")
            entry = EntryInfo(
                *struct.unpack(
                    "<iIiI", data[offset : offset + ENTRY_INFO_SIZE]
                )
            )
            package_entry_list.append(entry)
            offset += ENTRY_INFO_SIZE

        if package_value_length >= HEADER_MAX_BYTES:
            raise ValueError(
                f"Blob size({package_value_length}) BAD"
                f", 8 + 16 * il({idle_length}) + dl({data_length_})"
            )

        blob = HdrBlob(
            package_entry_list=package_entry_list,
            idle_length=idle_length,
            data_length=data_length_,
            package_value_length=package_value_length,
            data_start=data_start,
            data_end=data_end,
            region_tag=0,
            ril=0,
            rdl=0,
        )

        # Verify region and info if necessary, here shown as placeholders
        hdrblob_verify_region(blob, data)
        hdrblob_verify_info(blob, data)

        return blob

    except struct.error as exc:
        raise ValueError(f"Failed to parse structure: {str(exc)}") from exc
    except Exception as exc:
        raise ValueError(f"An error occurred: {str(exc)}") from exc


def htonl(val: int) -> int:
    # Pack integer as little-endian and then unpack as big-endian
    packed = struct.pack("<i", val)  # Little-endian int32
    return struct.unpack(">i", packed)[0]  # Big-endian int32


def htonl_u(val: int) -> int:
    # Pack unsigned integer as little-endian and then unpack as big-endian
    packed = struct.pack("<I", val)  # Little-endian uint32
    return struct.unpack(">I", packed)[0]  # Big-endian uint32


def ei2h(package_entry: EntryInfo) -> EntryInfo:
    return EntryInfo(
        type_=htonl_u(package_entry.type_),
        count=htonl_u(package_entry.count),
        offset=htonl(package_entry.offset),
        tag=htonl(package_entry.tag),
    )


def hdrchk_range(data_length_: int, offset: int) -> bool:
    return offset < 0 or offset > data_length_


def _hdrblob_verify_region_tag(entry_info: EntryInfo) -> None:
    if not (
        entry_info.type_ == REGION_TAG_TYPE
        and entry_info.count == REGION_TAG_COUNT
    ):
        raise ValueError("Invalid region tag")


def _hdrblob_verify_region_offset(data: bytes, region_end: int) -> None:
    if region_end > len(data) or region_end + REGION_TAG_COUNT > len(data):
        raise ValueError("Invalid region offset")


def hdrblob_verify_region(blob: HdrBlob, data: bytes) -> None:
    entry_info = ei2h(blob.package_entry_list[0])
    region_tag = None

    if entry_info.tag in {
        RPMTAG_HEADERIMAGE,
        RPMTAG_HEADERSIGNATURES,
        RPMTAG_HEADERIMMUTABLE,
    }:
        region_tag = entry_info.tag

    if entry_info.tag != region_tag:
        return

    _hdrblob_verify_region_tag(entry_info)

    if hdrchk_range(blob.data_length, entry_info.offset + REGION_TAG_COUNT):
        raise ValueError("Invalid region offset")

    region_end = blob.data_start + entry_info.offset
    _hdrblob_verify_region_offset(data, region_end)

    try:
        trailer_format = f"{REGION_TAG_COUNT}s"
        trailer_data = struct.unpack_from(
            "<" + trailer_format, data, region_end
        )
        trailer = EntryInfo(*struct.unpack("<iIii", trailer_data[0]))
        blob.rdl = region_end + REGION_TAG_COUNT - blob.data_start
    except struct.error as exc:
        raise ValueError(f"Failed to parse trailer: {str(exc)}") from exc

    if (
        region_tag == RPMTAG_HEADERSIGNATURES
        and entry_info.tag == RPMTAG_HEADERIMAGE
    ):
        entry_info.tag = RPMTAG_HEADERSIGNATURES

    if not (
        entry_info.tag == region_tag
        and entry_info.type_ == REGION_TAG_TYPE
        and entry_info.count == REGION_TAG_COUNT
    ):
        raise ValueError("Invalid region trailer")

    entry_info = ei2h(trailer)
    entry_info.offset = -entry_info.offset
    blob.ril = (
        entry_info.offset // ENTRY_INFO_SIZE
    )  # Adjust struct format as necessary
    if (
        (entry_info.offset % REGION_TAG_COUNT) != 0
        or hdrchk_range(blob.idle_length, blob.ril)
        or hdrchk_range(blob.data_length, blob.rdl)
    ):
        raise ValueError(f"Invalid region size, region {region_tag}")

    blob.region_tag = region_tag


def hdrchk_tag(tag: int) -> bool:
    # Replace HEADER_I18NTABLE with the actual constant value
    return tag < HEADER_I18NTABLE


def hdrchk_type(type_: int) -> bool:
    # Replace RPM_MIN_TYPE and RPM_MAX_TYPE with their actual values
    return type_ < RPM_MIN_TYPE or type_ > RPM_MAX_TYPE


def hdrchk_align(type_: int, offset: int) -> bool:
    # Replace typeAlign[t] with the actual alignment requirement for the type
    # Example: Assume typeAlign is a list where index represents type
    # and value represents alignment
    return offset & (TYPE_ALIGN[type_] - 1) != 0


def hdrblob_verify_info(blob: HdrBlob, data: bytes) -> None:
    end = 0
    package_offset = 1 if blob.region_tag != 0 else 0

    for package_entry in blob.package_entry_list[package_offset:]:
        info = ei2h(package_entry)

        if end > info.offset:
            raise ValueError(f"Invalid offset info: {info}")

        if hdrchk_tag(info.tag):
            raise ValueError(f"Invalid tag info: {info}")

        if hdrchk_type(info.type_):
            raise ValueError(f"Invalid type info: {info}")

        if hdrchk_align(info.type_, info.offset):
            raise ValueError(f"Invalid align info: {info}")

        if hdrchk_range(blob.data_length, info.offset):
            raise ValueError(f"Invalid range info: {info}")

        length = data_length(
            data,
            info.type_,
            info.count,
            blob.data_start + info.offset,
            blob.data_end,
        )
        end = info.offset + length

        if hdrchk_range(blob.data_length, end) or length <= 0:
            raise ValueError(f"Invalid data length info: {info}")


def data_length(
    data: bytes, type_: int, count: int, data_start: int, data_end: int
) -> int:
    length = 0
    if type_ == RPM_STRING_TYPE:
        if count != 1:
            return -1
        length = strtaglen(data, 1, data_start, data_end)
    elif type_ in (RPM_STRING_ARRAY_TYPE, RPM_I18NSTRING_TYPE):
        length = strtaglen(data, count, data_start, data_end)
    else:
        if TYPE_SIZES[type_] == -1:
            return -1
        length = TYPE_SIZES[type_ & 0xF] * int(count)
        if (length < 0) or ((data_start + length) > data_end > 0):
            return -1
    return length


def align_diff(type_: int, align_size: int) -> int:
    type_size = TYPE_SIZES[type_]
    if type_size > 1:
        diff = type_size - (align_size % type_size)
        if diff != type_size:
            return diff
    return 0


def strtaglen(data: bytes, count: int, start: int, data_end: int) -> int:
    length = 0
    if start >= data_end or data_end > len(data):
        return -1

    for _ in range(count):
        offset = start + length
        if offset >= len(data):
            return -1
        next_zero = data[offset:data_end].find(b"\x00") + 1
        if (
            next_zero == 0
        ):  # Find returns -1 when 0x00 is not found, hence +1 results in 0
            return -1
        length += next_zero
    return length


def _hdrblob_import_validate_data_len(rdlen: int, blob: HdrBlob) -> None:
    if rdlen != blob.data_length:
        raise ValueError(
            (
                f"the calculated length ({rdlen}) is different"
                f" from the data length ({blob.data_length})"
            )
        )


def _hdrblob_import_validate_rdlen(rdlen: int, message: str) -> None:
    if rdlen < 0:
        raise ValueError(message)


def hdrblob_import(blob: HdrBlob, data: bytes) -> list[IndexEntry]:
    index_entries: list[IndexEntry] = []
    dribble_index_entries: list[IndexEntry] = []

    entry = ei2h(blob.package_entry_list[0])
    if entry.tag >= RPMTAG_HEADERI18NTABLE:
        # An original v3 header, create a legacy region entry for it
        try:
            index_entries, rdlen = region_swab(
                data,
                blob.package_entry_list,
                0,
                blob.data_start,
                blob.data_end,
            )
        except Exception as exc:
            raise ValueError(
                f"failed to parse legacy index entries: {str(exc)}"
            ) from exc
    else:
        # Either a v4 header or an "upgraded" v3 header with a legacy region
        ril = blob.ril if entry.offset == 0 else blob.idle_length

        try:
            index_entries, rdlen = region_swab(
                data,
                blob.package_entry_list[1:ril],
                0,
                blob.data_start,
                blob.data_end,
            )
            _hdrblob_import_validate_rdlen(rdlen, "invalid region length")
        except Exception as exc:
            raise ValueError(
                f"failed to parse region entries: {str(exc)}"
            ) from exc

        if blob.ril < len(blob.package_entry_list) - 1:
            try:
                dribble_index_entries, rdlen = region_swab(
                    data,
                    blob.package_entry_list[ril:],
                    rdlen,
                    blob.data_start,
                    blob.data_end,
                )
                _hdrblob_import_validate_rdlen(
                    rdlen, "invalid length of dribble entries"
                )
            except Exception as exc:
                raise ValueError(
                    f"failed to parse dribble entries: {str(exc)}"
                ) from exc

            unique_tag_map = {
                index_entry.info.tag: index_entry
                for index_entry in index_entries + dribble_index_entries
            }
            index_entries = list(unique_tag_map.values())

        # The size calculation of other components is failing
        # rdlen += REGION_TAG_COUNT

    _hdrblob_import_validate_data_len(rdlen, blob)

    return index_entries


def region_swab(
    data: bytes,
    package_entries: list[EntryInfo],
    data_len: int,
    data_start: int,
    data_end: int,
) -> tuple[list[IndexEntry], int]:
    index_entries: list[IndexEntry] = []
    for index, package_entry_info in enumerate(package_entries):
        index_entry = IndexEntry(
            info=ei2h(package_entry_info), length=0, data=b"", rdlen=0
        )

        start = data_start + index_entry.info.offset
        if start >= data_end:
            raise ValueError("invalid data offset")

        if (
            index < len(package_entries) - 1
            and TYPE_SIZES[index_entry.info.type_] == -1
        ):
            next_offset = htonl(package_entries[index + 1].offset)
            index_entry.length = int(next_offset - index_entry.info.offset)
        else:
            index_entry.length = data_length(
                data,
                index_entry.info.type_,
                index_entry.info.count,
                start,
                data_end,
            )

        if index_entry.length < 0:
            raise ValueError("invalid data length")

        end = start + index_entry.length
        if start > len(data) or end > len(data):
            raise ValueError("invalid data length")

        index_entry.data = data[start:end]
        index_entries.append(index_entry)

        data_len += index_entry.length + align_diff(
            index_entry.info.type_, data_len
        )

    return index_entries, data_len


def header_import(data: bytes) -> list[IndexEntry]:
    blob = hdrblob_init(data)
    indexed_entries = hdrblob_import(blob, data)

    return indexed_entries


def get_digest_algorithm(value: int) -> str:
    result = "unknown-digest-algorithm"
    match value:
        case 1:
            result = "md5"
        case 2:
            result = "sha1"
        case 3:
            result = "ripemd160"
        case 5:
            result = "md2"
        case 6:
            result = "tiger192"
        case 7:
            result = "haval-5-160"
        case 8:
            result = "sha256"
        case 9:
            result = "sha384"
        case 10:
            result = "sha512"
        case 11:
            result = "sha224"
    return result


def validate_entry_type(
    index_entry: IndexEntry, tag_name: str, *required_type: int
) -> None:
    if index_entry.info.type_ not in required_type:
        raise ValueError(f"Invalid tag {tag_name}")


def _set_pkg_dir_indexes(
    pkg_info: PackageInfo, index_entry: IndexEntry
) -> None:
    validate_entry_type(index_entry, "dir_indexes", RPM_INT32_TYPE)
    pkg_info.dir_indexes = parse_int32_array(index_entry.data)


def _set_pkg_dir_names(pkg_info: PackageInfo, index_entry: IndexEntry) -> None:
    validate_entry_type(index_entry, "dir_names", RPM_STRING_ARRAY_TYPE)
    pkg_info.dir_names = parse_string_array(index_entry.data)


def _set_pkg_base_names(
    pkg_info: PackageInfo, index_entry: IndexEntry
) -> None:
    validate_entry_type(index_entry, "base_names", RPM_STRING_ARRAY_TYPE)
    pkg_info.base_names = parse_string_array(index_entry.data)


def _set_pkg_modularitylabel(
    pkg_info: PackageInfo, index_entry: IndexEntry
) -> None:
    validate_entry_type(index_entry, "modularitylabel", RPM_STRING_TYPE)
    pkg_info.modularitylabel = index_entry.data.rstrip(b"\x00").decode("utf-8")


def _set_pkg_name(pkg_info: PackageInfo, index_entry: IndexEntry) -> None:
    validate_entry_type(index_entry, "name", RPM_STRING_TYPE)
    pkg_info.name = index_entry.data.rstrip(b"\x00").decode("utf-8")


def _set_pkg_epoch(pkg_info: PackageInfo, index_entry: IndexEntry) -> None:
    validate_entry_type(index_entry, "epoch", RPM_INT32_TYPE)
    if index_entry.data:
        if value := parse_int32(index_entry.data):
            pkg_info.epoch = value
        else:
            raise ValueError("Failed to parse epoch")


def _set_pkg_version(pkg_info: PackageInfo, index_entry: IndexEntry) -> None:
    validate_entry_type(index_entry, "version", RPM_STRING_TYPE)
    pkg_info.version = index_entry.data.rstrip(b"\x00").decode("utf-8")


def _set_pkg_release(pkg_info: PackageInfo, index_entry: IndexEntry) -> None:
    validate_entry_type(index_entry, "release", RPM_STRING_TYPE)
    pkg_info.release = index_entry.data.rstrip(b"\x00").decode("utf-8")


def _set_pkg_arch(pkg_info: PackageInfo, index_entry: IndexEntry) -> None:
    validate_entry_type(index_entry, "arch", RPM_STRING_TYPE)
    pkg_info.arch = index_entry.data.rstrip(b"\x00").decode("utf-8")


def _set_pkg_source_rpm(
    pkg_info: PackageInfo, index_entry: IndexEntry
) -> None:
    validate_entry_type(index_entry, "source_rpm", RPM_STRING_TYPE)
    pkg_info.source_rpm = index_entry.data.rstrip(b"\x00").decode("utf-8")
    if pkg_info.source_rpm == "(none)":
        pkg_info.source_rpm = ""


def _set_pkg_provides(pkg_info: PackageInfo, index_entry: IndexEntry) -> None:
    validate_entry_type(index_entry, "provides", RPM_STRING_ARRAY_TYPE)
    pkg_info.provides = parse_string_array(index_entry.data)


def _set_pkg_requires(pkg_info: PackageInfo, index_entry: IndexEntry) -> None:
    validate_entry_type(index_entry, "requires", RPM_STRING_ARRAY_TYPE)
    pkg_info.requires = parse_string_array(index_entry.data)


def _set_pkg_license(pkg_info: PackageInfo, index_entry: IndexEntry) -> None:
    validate_entry_type(index_entry, "license", RPM_STRING_TYPE)
    pkg_info.license = index_entry.data.rstrip(b"\x00").decode("utf-8")
    if pkg_info.license == "(none)":
        pkg_info.license = ""


def _set_pkg_vendor(pkg_info: PackageInfo, index_entry: IndexEntry) -> None:
    validate_entry_type(index_entry, "vendor", RPM_STRING_TYPE)
    pkg_info.vendor = index_entry.data.rstrip(b"\x00").decode("utf-8")
    if pkg_info.vendor == "(none)":
        pkg_info.vendor = ""


def _set_pkg_size(pkg_info: PackageInfo, index_entry: IndexEntry) -> None:
    validate_entry_type(index_entry, "size", RPM_INT32_TYPE)
    if value := parse_int32(index_entry.data):
        pkg_info.size = value


def _set_pkg_digest_algorithm(
    pkg_info: PackageInfo, index_entry: IndexEntry
) -> None:
    validate_entry_type(index_entry, "digest_algorithm", RPM_INT32_TYPE)
    if value := parse_int32(index_entry.data):
        pkg_info.digest_algorithm = get_digest_algorithm(value)


def _set_pkg_file_sizes(
    pkg_info: PackageInfo, index_entry: IndexEntry
) -> None:
    validate_entry_type(index_entry, "file_sizes", RPM_INT32_TYPE)
    if file_sizes := parse_int32_array(index_entry.data):
        pkg_info.file_sizes = file_sizes


def _set_pkg_file_digests(
    pkg_info: PackageInfo, index_entry: IndexEntry
) -> None:
    validate_entry_type(index_entry, "file_digests", RPM_STRING_ARRAY_TYPE)
    pkg_info.file_digests = parse_string_array(index_entry.data)


def _set_pkg_file_modes(
    pkg_info: PackageInfo, index_entry: IndexEntry
) -> None:
    validate_entry_type(index_entry, "file_modes", RPM_INT16_TYPE)
    if file_modes := uint16_array(index_entry.data):
        pkg_info.file_modes = file_modes


def _set_pkg_file_flags(
    pkg_info: PackageInfo, index_entry: IndexEntry
) -> None:
    validate_entry_type(index_entry, "file_flags", RPM_INT32_TYPE)
    if file_flags := parse_int32_array(index_entry.data):
        pkg_info.file_flags = file_flags


def _set_pkg_user_names(
    pkg_info: PackageInfo, index_entry: IndexEntry
) -> None:
    validate_entry_type(index_entry, "file_user_names", RPM_STRING_ARRAY_TYPE)
    pkg_info.user_names = parse_string_array(index_entry.data)


def _set_pkg_summary(pkg_info: PackageInfo, index_entry: IndexEntry) -> None:
    validate_entry_type(
        index_entry, "summary", RPM_STRING_TYPE, RPM_I18NSTRING_TYPE
    )
    pkg_info.summary = index_entry.data.split(b"\x00", 1)[0].decode("utf-8")


def _set_pkg_install_time(
    pkg_info: PackageInfo, index_entry: IndexEntry
) -> None:
    if index_entry.info.type_ != RPM_INT32_TYPE:
        raise ValueError("Invalid tag install time")
    if value := parse_int32(index_entry.data):
        pkg_info.install_time = value


def _set_pkg_sig_md5(pkg_info: PackageInfo, index_entry: IndexEntry) -> None:
    pkg_info.sig_md5 = index_entry.data.hex()


def get_package_info(index_entries: list[IndexEntry]) -> PackageInfo:
    pkg_info = PackageInfo()
    tag_to_function_map = {
        1116: _set_pkg_dir_indexes,
        1118: _set_pkg_dir_names,
        1117: _set_pkg_base_names,
        5096: _set_pkg_modularitylabel,
        1000: _set_pkg_name,
        1003: _set_pkg_epoch,
        1001: _set_pkg_version,
        1002: _set_pkg_release,
        1022: _set_pkg_arch,
        1044: _set_pkg_source_rpm,
        1047: _set_pkg_provides,
        1049: _set_pkg_requires,
        1014: _set_pkg_license,
        1011: _set_pkg_vendor,
        1009: _set_pkg_size,
        5011: _set_pkg_digest_algorithm,
        1028: _set_pkg_file_sizes,
        1035: _set_pkg_file_digests,
        1030: _set_pkg_file_modes,
        1037: _set_pkg_file_flags,
        1039: _set_pkg_user_names,
        1004: _set_pkg_summary,
        1008: _set_pkg_install_time,
        261: _set_pkg_sig_md5,
    }
    for index_entry in index_entries:
        if index_entry.info.tag in tag_to_function_map:
            tag_to_function_map[index_entry.info.tag](pkg_info, index_entry)
    return pkg_info
