# noqa: S5843
import abc
import re
import sys
from typing import (
    cast,
    SupportsInt,
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


class Pep440VersionScheme(ISchemeFactory):
    @property
    def clear_value(self) -> int | None:
        return 0

    def clear_value_map(self, item: str) -> tuple[str, int]:
        if item in ("a", "b", "dev"):
            return ("post", sys.maxsize)
        if item == "post":
            return ("post", -1)
        if item == "local":
            return ("a", 0)
        if item == "rc":
            return ("rc", sys.maxsize)
        return ("post", sys.maxsize)

    def _parse_letter_version(
        self,
        letter: str | None,
        number: str | bytes | SupportsInt | None,
    ) -> list[str | int] | None:
        if letter and isinstance(letter, str):
            if number is None:
                number = 0

            letter = letter.lower()

            if letter == "alpha":
                letter = "a"
            elif letter == "beta":
                letter = "b"
            elif letter in ["c", "pre", "preview"]:
                letter = "rc"
            elif letter in ["rev", "r"]:
                letter = "post"

            return [letter, int(number)]
        if not letter and number:
            letter = "post"

            return [letter, int(number)]

        return None

    def _parse_local_version(
        self, local: str | None
    ) -> list[int | str] | None:
        """
        Takes a string like abc.1.twelve and turns it into ("abc", 1, "twelve")
        """
        _local_version_separators = re.compile(r"[\._-]")
        if local is not None:
            return list(
                part.lower() if not part.isdigit() else int(part)
                for part in cast(
                    list[str], _local_version_separators.split(local)
                )
            )

        return None

    def parse(
        self,
        version: str,
    ) -> list[str | int | list[str | int | None] | None] | None:
        epoch_regex = r"(?:(?P<epoch>\d+)!)?"  # epoch
        release_regex = r"(?P<release>\d+(?:\.\d+)*)"  # release segment

        pre_regex = r"""
            (?P<pre>
                [-_\.]?(?P<pre_l>(alpha|beta|pre|preview|rc|a|b|c))
                ([-_\.]?(?P<pre_n>\d+))?
            )?
        """

        post_regex = r"""
            (?P<post>
                (?:-(?P<post_n1>\d+))
                |
                (?:
                    [-_\.]?
                    (?P<post_l>post|rev|r)
                    [-_\.]?
                    (?P<post_n2>\d+)?
                )
            )?
        """

        dev_regex = r"""
            (?P<dev>
                [-_\.]?
                (?P<dev_l>dev)
                [-_\.]?
                (?P<dev_n>\d+)?
            )?
        """

        local_regex = r"""
            (?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?  # local version
        """
        regex_expresion = (
            r"v?"
            + epoch_regex
            + release_regex
            + pre_regex
            + post_regex
            + dev_regex
            + local_regex
        )
        pattern = re.compile(regex_expresion, re.VERBOSE)
        match = pattern.match(version)
        if not match:
            return None
        match_dict: dict[str, str | None] = match.groupdict()
        result: list[str | int | list[str | int | None] | None] = [
            int(match_dict.get("epoch") or 0),  # epoch
            [
                int(x) for x in (match_dict.get("release") or "0").split(".")
            ],  # release
            self._parse_letter_version(  # type: ignore
                match_dict.get("pre_l"), match_dict.get("pre_n")
            ),
            self._parse_letter_version(  # type: ignore
                match_dict.get("post_l"),
                match_dict.get("post_n1") or match_dict.get("post_n2"),
            ),
            self._parse_letter_version(  # type: ignore
                match_dict.get("dev_l"), match_dict.get("dev_n")
            ),
            self._parse_local_version(match_dict.get("local")),  # type: ignore
        ]

        return result
