import atexit
import boto3
from botocore import (
    UNSIGNED,
)
from botocore.config import (
    Config,
)
from botocore.exceptions import (
    ClientError,
)
from cpe import (
    CPE,
)
from fluid_sbom.advisories.schemes import (
    DebianVersionScheme,
    SemVerVersionScheme,
)
from fluid_sbom.pkg.language import (
    Language,
)
from fluid_sbom.pkg.package import (
    Advisory,
    Package,
)
from fluid_sbom.pkg.type import (
    PackageType,
)
import json
import logging
import os
from packageurl import (
    PackageURL,
)
from platformdirs import (
    user_data_dir,
)
import re
import semver
import sqlite3
import subprocess
from tqdm import (
    tqdm,
)
from typing import (
    cast,
    Literal,
)
from versio.version import (
    Version,
)
from versio.version_scheme import (
    Pep440VersionScheme,
    VersionScheme,
)

BUCKET_NAME = "fluidattacks.public.storage"
DB_NAME = "vulnerability.db"
FILE_KEY = f"sbom/{DB_NAME}.zst"
CONFIG_DIRECTORY = user_data_dir(
    appname="fluid-sbom",
    appauthor="fluidattacks",
    ensure_exists=True,
)
DB_PATH = os.path.join(CONFIG_DIRECTORY, DB_NAME)
DB_COMPRESSED_PATH = f"{DB_PATH}.zst"

LOGGER = logging.getLogger(__name__)
S3_SERVICE_NAME: Literal["s3"] = "s3"
S3_CLIENT = boto3.client(
    service_name=S3_SERVICE_NAME,
    config=Config(
        region_name="us-east-1",
        signature_version=UNSIGNED,  # type: ignore[misc]
    ),
)


def _download_database_file(download_size: float) -> None:
    LOGGER.info("⬇️ Downloading advisories database")
    with tqdm(
        leave=False,
        total=download_size,
        unit="B",
        unit_scale=True,
    ) as progress_bar:
        S3_CLIENT.download_file(
            Bucket=BUCKET_NAME,
            Callback=progress_bar.update,
            Filename=DB_COMPRESSED_PATH,
            Key=FILE_KEY,
        )


def _decompress_database_file() -> None:
    LOGGER.info("🗜️ Decompressing advisories database")
    with subprocess.Popen(
        ["zstd", "-d", "-f", DB_COMPRESSED_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as process:
        _, stderr = process.communicate()
        if cast(int, process.returncode) != 0:
            raise RuntimeError(stderr.decode())


def _is_database_available() -> bool:
    local_database_exists = os.path.isfile(DB_PATH)

    try:
        db_metadata = S3_CLIENT.head_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
        up_to_date = (
            local_database_exists
            and os.path.getmtime(DB_PATH)
            >= db_metadata["LastModified"].timestamp()
        )

        if up_to_date:
            LOGGER.info("✅ Advisories database is up to date")
            return True

        _download_database_file(db_metadata["ContentLength"])
        _decompress_database_file()
        os.unlink(DB_COMPRESSED_PATH)
        return True
    except (ClientError, RuntimeError):  # type: ignore[misc]
        if local_database_exists:
            LOGGER.warning(
                "⚠️ Advisories may be outdated, unable to update database",
            )
            return True

        LOGGER.exception(
            "❌ Advisories won't be included, unable to download database",
        )
        return False


class DatabaseContext:
    def __init__(self) -> None:
        self.connection: sqlite3.Connection | None = None

    def initialize(self) -> None:
        if self.connection is None and _is_database_available():
            self.connection = sqlite3.connect(
                DB_PATH,
                # Should be OK as we are only reading, not writing
                check_same_thread=False,
            )
            atexit.register(self.connection.close)

    def get_connection(self) -> sqlite3.Connection | None:
        return self.connection


_database_context = DatabaseContext()
initialize_database = _database_context.initialize


class GrypeDbVersion(semver.Version):
    """
    Some modifications to make it complatible with their version format

    https://github.com/anchore/go-version
    """

    # Needed while https://github.com/python-semver/python-semver/pull/367
    # pylint: disable=protected-access
    _REGEX_TEMPLATE = semver.Version._REGEX_TEMPLATE.replace("^", r"^(\^|~)?")
    _REGEX = re.compile(
        _REGEX_TEMPLATE.format(opt_patch="", opt_minor=""),
        re.VERBOSE,
    )
    _REGEX_OPTIONAL_MINOR_AND_PATCH = re.compile(
        _REGEX_TEMPLATE.format(opt_patch="?", opt_minor="?"),
        re.VERBOSE,
    )

    def compare(self, other: semver.version.Comparable) -> int:
        cls = type(self)
        if isinstance(other, str):
            return super().compare(
                cls.parse(other, optional_minor_and_patch=True)
            )
        return super().compare(other)

    def match(self, match_expr: str) -> bool:
        without_spaces = match_expr.replace(" ", "")
        with_double_equals = (
            without_spaces.replace("=", "==")
            if without_spaces.startswith("=")
            and without_spaces.count("=") == 1
            else without_spaces
        )

        if with_double_equals[0] == "^":
            return super().parse(with_double_equals[1:]).major == self.major
        if with_double_equals[0] == "~":
            parsed = super().parse(with_double_equals[1:])
            return parsed.major == self.major and parsed.minor == self.minor

        return super().match(with_double_equals)


def _get_target_software(cpe: str) -> list[str]:
    return cast(
        list[str],
        CPE(cpe).get_target_software(),  # type: ignore[misc]
    )


def _matches_cpe(package: Package, advisory: Advisory) -> bool:
    mapping: dict[Language, list[str]] = {
        Language.DART: ["dart"],
        Language.DOTNET: [".net", "asp.net"],
        Language.GO: ["go", "golang"],
        Language.JAVA: ["java"],
        Language.JAVASCRIPT: ["javascript", "node.js", "nodejs"],
        Language.PHP: ["php"],
        Language.PYTHON: ["pypi", "python"],
        Language.RUBY: ["rails", "ruby", "ruby_on_rails"],
        Language.RUST: ["rust"],
        Language.SWIFT: ["swift"],
    }

    return package.language in mapping and any(
        target_software in mapping[package.language]
        for cpe in advisory.cpes
        for target_software in _get_target_software(cpe)
    )


def _matches_ghsa(package: Package, advisory: Advisory) -> bool:
    namespace_type = advisory.namespace.split(":")[1]
    if namespace_type == "language":
        return package.language.value in (
            "dotnet",
            "go",
            "java",
            "javascript",
            "php",
            "python",
            "ruby",
            "rust",
            "swift",
        )

    if namespace_type == "distro":
        return package.type in (PackageType.DebPkg,)

    return False


def _matches_platform(package: Package, advisory: Advisory) -> bool:
    return _matches_ghsa(package, advisory) or _matches_cpe(package, advisory)


def version_match_constraint(version: Version, constraint: str) -> bool:
    if not constraint:
        return True
    constraints = constraint.split("||")
    result = any(
        _compare_single_constraint(version, constraint.strip(), version.scheme)
        for constraint in constraints
    )
    return result


def _compare_single_constraint(
    version: Version, constraint: str, scheme: VersionScheme
) -> bool:
    match = re.match(r"([<>=~!^]*)(.*)", constraint)
    if not match:
        raise ValueError(f"Invalid constraint: {constraint}")
    groups: tuple[str, str] = match.groups()  # type: ignore
    operator, constraint_version = groups
    operator = operator or "=="  # Assume equality if no explicit operator

    other = Version(constraint_version.strip(), scheme=scheme)

    def less_than(version_1: Version, version_2: Version) -> bool:
        return version_1 < version_2

    def greater_than(version_1: Version, version_2: Version) -> bool:
        return version_1 > version_2

    def less_than_or_equal(version_1: Version, version_2: Version) -> bool:
        return version_1 <= version_2

    def greater_than_or_equal(version_1: Version, version_2: Version) -> bool:
        return version_1 >= version_2

    def equal(version_1: Version, version_2: Version) -> bool:
        return version_1 == version_2

    operators = {
        "<": less_than,
        ">": greater_than,
        "<=": less_than_or_equal,
        ">=": greater_than_or_equal,
        "==": equal,
        "=": equal,
    }

    if operator not in operators:
        raise ValueError(f"Invalid operator: {operator}")

    return operators[operator](version, other)


def _get_version_scheme_by_namespace(namespace: str) -> VersionScheme | None:
    namespace_type = namespace.split(":")[1]
    scheme: VersionScheme | None = None
    if namespace_type == "language":
        language = namespace.split(":")[2]
        if language == "python":
            scheme = Pep440VersionScheme
        elif language in (
            "javascript",
            "ruby",
            "rust",
            "dotnet",
            "swift",
            "dart",
        ):
            scheme = SemVerVersionScheme
    elif namespace_type == "distro":
        distro_name = namespace.split(":")[2]
        if distro_name == "debian":
            scheme = DebianVersionScheme
    return scheme


def _matches_version(package: Package, advisory: Advisory) -> bool:
    scheme = _get_version_scheme_by_namespace(advisory.namespace)
    if scheme is None:
        LOGGER.warning(
            "No version scheme found for namespace %s",
            advisory.namespace,
        )
        return False
    try:
        return all(
            version_match_constraint(
                Version(package.version, scheme=scheme), comparator
            )
            for comparator in advisory.version_constraint.split(",")
        )

    except AttributeError:
        return False


def _matches(package: Package, advisory: Advisory) -> bool:
    return _matches_platform(package, advisory) and _matches_version(
        package, advisory
    )


AdvisoryRow = tuple[
    str, str, str, str, str, float | None, float | None, str, str
]


def _format_advisory(row: AdvisoryRow) -> Advisory:
    return Advisory(
        cpes=cast(list[str], json.loads(row[0] or "[]")),
        description=row[4],
        epss=row[5] or 0.0,
        id=row[1],
        namespace=row[2],
        percentile=row[6] or 0.0,
        severity=row[7],
        urls=cast(list[str], json.loads(row[8] or "[]")),
        version_constraint=row[3],
    )


def _get_matching_advisories(package: Package) -> list[Advisory]:
    connection = _database_context.get_connection()
    if connection is None:
        return []

    cursor = connection.cursor()
    if (
        package.p_url
        and (
            pacakge_url := PackageURL.from_string(  # type: ignore
                package.p_url,
            )
        )
        and isinstance(pacakge_url.qualifiers, dict)  # type: ignore
        and (distro := pacakge_url.qualifiers.get("distro"))  # type: ignore
    ):
        distro = f'%:distro:{distro.replace("-", ":")}'
        cursor.execute(
            """
            SELECT
                vuln.cpes,
                vuln.id,
                vuln.namespace,
                vuln.version_constraint,
                vuln_meta.description,
                vuln_meta.epss,
                vuln_meta.percentile,
                vuln_meta.severity,
                vuln_meta.urls
            FROM
                vulnerability vuln
            INNER JOIN vulnerability_metadata vuln_meta
                ON vuln.id = vuln_meta.id
                AND vuln.namespace = vuln_meta.namespace
            WHERE vuln.package_name = ?
            AND vuln.namespace LIKE ?
            """,
            (package.name, distro),
        )
    else:
        cursor.execute(
            """
        SELECT
            vuln.cpes,
            vuln.id,
            vuln.namespace,
            vuln.version_constraint,
            vuln_meta.description,
            vuln_meta.epss,
            vuln_meta.percentile,
            vuln_meta.severity,
            vuln_meta.urls
        FROM
            vulnerability vuln
        INNER JOIN vulnerability_metadata vuln_meta
            ON vuln.id = vuln_meta.id
            AND vuln.namespace = vuln_meta.namespace
        WHERE vuln.package_name = ?
        """,
            (package.name,),
        )

    result = [
        advisory
        for row in cast(list[AdvisoryRow], cursor.fetchall())
        if (advisory := _format_advisory(row)) and _matches(package, advisory)
    ]
    return result


def get_package_advisories(package: Package) -> list[Advisory]:
    try:
        return _get_matching_advisories(package)
    except Exception:  # pylint:disable=broad-exception-caught
        LOGGER.exception(
            "Unable to get advisories for package %s",
            package.name,
        )
        return []
