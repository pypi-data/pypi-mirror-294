import re
from versio.version_scheme import (
    VersionScheme,
)

SemVerVersionScheme = VersionScheme(
    name="semver",
    parse_regex=r"""
    ^
    (?P<major>\d+)\.
    (?P<minor>\d+)\.
    (?P<patch>\d+)
    (?:-(?P<pre>[0-9A-Za-z\-\.]+))?
    (?:\+(?P<build>[0-9A-Za-z\-\.]+))?
    $
    """,
    compare_order=[0, 1, 2, 3, 4],
    compare_fill=[None, None, None, "~", "~"],
    parse_flags=re.VERBOSE,
    clear_value=None,
    format_str="{major}.{minor}.{patch}{pre}{build}",
    fields=["major", "minor", "patch", "pre", "build"],
    subfields={},
    sequences={"pre": ["alpha", "beta", "rc"], "build": ["+"]},
    description="""
        SemVer (Semantic Versioning)
        Version format: MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]

        MAJOR, MINOR, PATCH are required numeric fields.
        PRERELEASE is an optional field that can contain alphanumeric
        characters and dots, separated by a hyphen from the PATCH field.
        BUILD is an optional field that can contain alphanumeric characters
        and dots, separated by a plus sign from the PATCH or PRERELEASE field.
    """,
)

DebianVersionScheme = VersionScheme(
    name="debian",
    parse_regex=r"""
        ^(?:(?P<Epoch>\d+):)?  # Optional Epoch
        (?P<Major>\d+)(?:\.(?P<Minor>\d+))?(?:\.(?P<Patch>\d+))?(?:[\-\+\~])?
        (?P<Rest>[\w\.\~\+]*)  # Mandatory Upstream Version
        (?:-(?P<DebianRevision>[\w\.\+\-~]+))?$  # Optional Debian Revision
    """,
    parse_flags=re.VERBOSE,
    format_str="{Epoch}:{UpstreamVersion}-{DebianRevision}",
    fields=["Epoch", "Major", "Minor", "Patch", "Rest", "DebianRevision"],
    clear_value="0",
    sequences={
        "Epoch": ["0"],
        "Major": ["1"],
        "Minor": ["2"],
        "Patch": ["3"],
        "Rest": ["4"],
        "DebianRevision": ["5"],
    },
)
