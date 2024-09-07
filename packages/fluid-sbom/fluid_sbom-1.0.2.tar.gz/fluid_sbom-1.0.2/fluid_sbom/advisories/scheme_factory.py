# pylint: disable=protected-access
from __future__ import (
    annotations,
)

import abc
from packaging._structures import (
    Infinity,
    NegativeInfinity,
)
from packaging.version import (
    parse as parse_pypi,
    Version as PypiVersion,
)
import re
from semver import (
    Version as SemVerVersion,
)


class ISchemeFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(
        self,
        version: str,
    ) -> list[str | int | list[int | str | None] | None] | None:
        """Resolve file context"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def clear_value(
        self,
    ) -> int | None:
        """Resolve file context"""
        raise NotImplementedError

    @abc.abstractmethod
    def clear_value_map(self, item: str) -> tuple[str, int]:
        """Return the name of the version scheme"""
        raise NotImplementedError

    @abc.abstractmethod
    def compare(self, other: str) -> int:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def raw_version(self) -> str:
        raise NotImplementedError


class Pep440VersionScheme(ISchemeFactory):
    version_item: PypiVersion

    @property
    def clear_value(self) -> int | None:
        return 0

    @property
    def raw_version(self) -> str:
        return self.raw_version

    @raw_version.setter
    def raw_version(self, value: str) -> None:
        self._raw_version = value

    def clear_value_map(self, item: str) -> tuple[str, int]:
        raise NotImplementedError

    def parse(
        self,
        version: str,
    ) -> list[str | int | list[str | int | None] | None] | None:
        self.raw_version = version
        self.version_item = parse_pypi(version)
        return self.version_item._key  # type: ignore

    def compare(self, other: str) -> int:
        version_item = parse_pypi(other)
        if self.version_item < version_item:
            return -1
        if self.version_item > version_item:
            return 1
        return 0


class SemVerScheme(ISchemeFactory):
    version_item: SemVerVersion

    @property
    def clear_value(self) -> int | None:
        return 0

    def compare(self, other: str) -> int:
        return self.version_item.compare(other)

    def clear_value_map(self, item: str) -> tuple[str, int]:
        raise NotImplementedError

    @property
    def raw_version(self) -> str:
        return self.raw_version

    @raw_version.setter
    def raw_version(self, value: str) -> None:
        self._raw_version = value

    def parse(
        self,
        version: str,
    ) -> list[str | int | list[str | int | None] | None] | None:
        self.raw_version = version
        self.version_item = SemVerVersion.parse(version)
        return [
            self.version_item.major,
            self.version_item.minor,
            self.version_item.patch,
            self.version_item.prerelease,
            self.version_item.build,
        ]


class PhpComposerScheme(ISchemeFactory):
    def compare(self, other: str) -> int:
        raise NotImplementedError

    def clear_value_map(self, item: str) -> tuple[str, int]:
        raise NotImplementedError

    @property
    def clear_value(self) -> int | None:
        return 0

    @property
    def raw_version(self) -> str:
        return self.raw_version

    @raw_version.setter
    def raw_version(self, value: str) -> None:
        self._raw_version = value

    def parse(
        self, version: str
    ) -> list[str | int | list[int | str | None] | None] | None:
        pattern = r"""
        ^
        (?P<prefix>v?)
        (?P<major>\d+)
        \.(?P<minor>\d+)
        (?P<patch>\.\d+|\.x)
        (?:-(?P<suffix>dev|patch|p|alpha|a|beta|b|RC)
            (?P<number>\d+)?
        )?$
        """
        match = re.match(pattern, version, re.VERBOSE)
        if not match:
            raise ValueError(f"Invalid PHP version: {version}")
        match_dict: dict[str, str | None] = match.groupdict()
        major, minor, patch = self._parse_version_parts(match_dict)
        release = (major, minor, patch)
        pre = self._parse_pre_release(
            match_dict.get("suffix") or "", match_dict.get("number") or 0
        )

        _release = self._create_release(release)
        _pre = pre if pre is not None else Infinity
        _dev = NegativeInfinity  # Dev versions are handled in pre-release

        return [list(_release), _pre, _dev]  # type: ignore

    def _parse_version_parts(
        self, match: dict[str, str | None]
    ) -> tuple[int, int, int]:
        major = int(match.get("major", 0) or 0)
        minor = int(match.get("minor", 0) or 0)
        _patch = match.get("patch", "") or ""
        patch: int = 0 if _patch == ".x" else int(_patch.lstrip("."))
        return major, minor, patch

    def _parse_pre_release(
        self, suffix: str, number: int | str | None
    ) -> tuple[str | int] | None:
        if not suffix:
            return None

        pre_release_map = {
            "dev": ("", int(number) if number else -1),
            "patch": ("patch", int(number) if number else 0),
            "p": ("patch", int(number) if number else 0),
            "alpha": ("a", int(number) if number else 0),
            "a": ("a", int(number) if number else 0),
            "beta": ("b", int(number) if number else 0),
            "b": ("b", int(number) if number else 0),
            "RC": ("rc", int(number) if number else 0),
        }

        return pre_release_map.get(  # type: ignore
            suffix, (suffix, int(number) if number else 0)
        )

    def _create_release(self, release: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(
            reversed(
                list(
                    filter(
                        lambda x: x != 0,  # type: ignore
                        reversed(release),
                    ),
                ),
            )
        )
