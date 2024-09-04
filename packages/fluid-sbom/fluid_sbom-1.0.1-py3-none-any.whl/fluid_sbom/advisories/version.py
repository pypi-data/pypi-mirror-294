from __future__ import (
    annotations,
)

from fluid_sbom.advisories.scheme_factory import (
    ISchemeFactory,
)
from typing import (
    Callable,
)

TItem = str | int | None


def _cmp(a_item: TItem, b_item: TItem) -> int:
    if a_item is None and b_item is None:
        return 0

    if (isinstance(a_item, int) and isinstance(b_item, int)) or (
        isinstance(a_item, str) and isinstance(b_item, str)
    ):
        if a_item < b_item:  # type: ignore
            return -1
        if a_item > b_item:  # type: ignore
            return 1
        return 0

    raise TypeError(f"Can not compare {type(a_item)} and {type(b_item)}")


class Version:
    def __init__(self, version_string: str, scheme: ISchemeFactory) -> None:
        self.scheme = scheme
        self.parts = scheme.parse(version_string)
        self.value = version_string
        if not self.parts:
            raise AttributeError(
                f'Can not find supported scheme for "{version_string}"'
            )

    def _compare_sub_list(
        self,
        x_items: list[TItem] | tuple[TItem],
        y_items: list[TItem] | tuple[TItem],
        method: Callable[[TItem, TItem], bool],
    ) -> bool | None:
        for x_item, y_item in zip(x_items, y_items):
            try:
                result = self._compare_values(x_item, y_item, method)
            except StopIteration:
                continue
            if result is not None:
                return result
        raise StopIteration

    def _compare_values(
        self,
        x_item: TItem,
        y_item: TItem,
        method: Callable[[TItem, TItem], bool],
    ) -> bool | None:
        if (
            x_item is not None
            and y_item is not None
            and self._items_equal(x_item, y_item)
        ):
            raise StopIteration
        if x_item is None and y_item is None:
            raise StopIteration

        try:
            return method(int(x_item), int(y_item))  # type: ignore
        except (TypeError, ValueError):
            return method(str(x_item), str(y_item))

    def _items_equal(self, x_item: TItem, y_item: TItem) -> bool:
        if x_item is None and y_item is None:
            return True
        if x_item is None or y_item is None:
            raise TypeError("Can not compare None")

        try:
            return int(x_item) == int(y_item)
        except (TypeError, ValueError):
            return str(x_item) == str(y_item)

    def _apply_method(
        self,
        x_item: TItem,
        y_item: TItem,
        method: Callable[[TItem, TItem], bool],
    ) -> bool:
        if x_item is None or y_item is None:
            raise TypeError("Can not compare None")
        try:
            return method(int(x_item), int(y_item))
        except (TypeError, ValueError):
            return method(str(x_item), str(y_item))

    def _compare(
        self,
        other: Version | str,
        method: Callable[[TItem, TItem], bool],
    ) -> bool:
        _other: Version | str | None = None
        if not isinstance(other, Version):
            try:
                _other = Version(str(other), scheme=self.scheme)
            except AttributeError:
                return NotImplemented
        _other = _other or other
        if not isinstance(_other, Version):
            raise TypeError("other must be a Version instance or a string")
        if not self.parts or not _other.parts:
            raise AttributeError("parts is empty")
        try:
            return self._compare_keys(self.parts, _other.parts, method)
        except (AttributeError, TypeError):
            # _cmpkey not implemented, or return different type,
            # so I can't compare with "other".
            return NotImplemented

    def _normalice_items(
        self, x_item: TItem | list[TItem], y_item: TItem | list[TItem]
    ) -> tuple[list[TItem], list[TItem]]:
        if isinstance(x_item, (tuple, list)) and not isinstance(
            y_item, (tuple, list)
        ):
            result = self._handle_list_and_non_list(x_item, y_item)
        if isinstance(y_item, (tuple, list)) and not isinstance(
            x_item, (tuple, list)
        ):
            result = self._handle_list_and_non_list(
                y_item, x_item, reverse=True
            )
        if isinstance(x_item, (tuple, list)) and isinstance(
            y_item, (tuple, list)
        ):
            result = list(x_item), list(y_item)
        return result

    def _handle_list_and_non_list(
        self,
        list_item: list[TItem],
        non_list_item: TItem,
        reverse: bool = False,
    ) -> tuple[list[TItem], list[TItem]]:
        if non_list_item is None:
            if list_item and isinstance(list_item[0], str):
                _non_list_item = list(
                    self.scheme.clear_value_map(list_item[0])
                )
            else:
                raise TypeError(
                    (
                        "Unhandled conversion type "
                        f"{type(list_item)} and {type(non_list_item)}"
                    )
                )
        else:
            raise TypeError(
                (
                    "Unhandled conversion type "
                    f"{type(list_item)} and {type(non_list_item)}"
                )
            )
        result = (
            (_non_list_item, list(list_item))
            if reverse
            else (list(list_item), _non_list_item)
        )
        return result  # type: ignore

    def _compare_keys(
        self,
        x_cmpkey: list[TItem | list[TItem]],
        y_cmpkey: list[TItem | list[TItem]],
        method: Callable[[TItem, TItem], bool],
    ) -> bool:
        x_cmpkey, y_cmpkey = self._equalize_key_lengths(x_cmpkey, y_cmpkey)
        return self._compare_key_items(x_cmpkey, y_cmpkey, method)

    def _compare_key_items(
        self,
        x_cmpkey: list[TItem | list[TItem]],
        y_cmpkey: list[TItem | list[TItem]],
        method: Callable[[TItem, TItem], bool],
    ) -> bool:
        result_iteration = []
        for x_item, y_item in zip(x_cmpkey, y_cmpkey):
            try:
                result = self._compare_item_pair(x_item, y_item, method)
            except StopIteration:
                continue
            result_iteration.append(result)

            if result is not None:
                return result
        if all(x is None for x in result_iteration):
            return True

        return False

    def _compare_item_pair(
        self,
        x_item: TItem | list[TItem],
        y_item: TItem | list[TItem],
        method: Callable[[TItem, TItem], bool],
    ) -> bool | None:
        if (
            isinstance(x_item, (list, tuple))
            and not isinstance(y_item, (list, tuple))
        ) or (
            isinstance(y_item, (list, tuple))
            and not isinstance(x_item, (list, tuple))
        ):
            x_item, y_item = self._normalice_items(x_item, y_item)

        if isinstance(x_item, (list, tuple)) and isinstance(
            y_item, (list, tuple)
        ):
            return self._compare_sub_list(x_item, y_item, method)
        if isinstance(x_item, (list, tuple)) or isinstance(
            y_item, (list, tuple)
        ):
            raise TypeError(f"Can not compare {x_item} with {y_item}")

        return self._compare_values(x_item, y_item, method)

    def _equalize_key_lengths(
        self,
        x_cmpkey: list[TItem | list[TItem]],
        y_cmpkey: list[TItem | list[TItem]],
    ) -> tuple[list[TItem | list[TItem]], list[TItem | list[TItem]]]:
        max_length = max(len(x_cmpkey), len(y_cmpkey))
        x_cmpkey += [self.scheme.clear_value or 0] * (
            max_length - len(x_cmpkey)
        )
        y_cmpkey += [self.scheme.clear_value or 0] * (
            max_length - len(y_cmpkey)
        )
        return x_cmpkey, y_cmpkey

    def __lt__(self, other: Version | str) -> bool:
        return self._compare(other, lambda s, o: _cmp(s, o) < 0)

    def __le__(self, other: Version | str) -> bool:
        return self._compare(other, lambda s, o: _cmp(s, o) <= 0)

    def __eq__(self, other: Version | str) -> bool:  # type: ignore
        return self._compare(other, lambda s, o: _cmp(s, o) == 0)

    def __ge__(self, other: Version | str) -> bool:
        return self._compare(other, lambda s, o: _cmp(s, o) >= 0)

    def __gt__(self, other: Version | str) -> bool:
        return self._compare(other, lambda s, o: _cmp(s, o) > 0)

    def __ne__(self, other: Version) -> bool:  # type: ignore
        return self._compare(other, lambda s, o: _cmp(s, o) != 0)
