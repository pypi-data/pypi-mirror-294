from collections import (
    UserDict,
    UserList,
)
from tree_sitter import (
    Node,
)
from typing import (
    Any,
    NamedTuple,
)


class FileCoordinate(NamedTuple):
    line: int
    column: int


class Position(NamedTuple):
    start: FileCoordinate
    end: FileCoordinate


class IndexedDict(UserDict):
    def __init__(self, root_node: Node | None = None):
        self.position_value_index: dict[str, Position] = {}
        self.position_key_index: dict[str, Position] = {}
        data: dict[tuple[str, Position], tuple[Any, Position]] = {}
        if root_node:
            self.position = Position(
                FileCoordinate(
                    root_node.start_point[0] + 1,
                    root_node.start_point[1] + 1,
                ),
                FileCoordinate(
                    root_node.end_point[0] + 1,
                    root_node.end_point[1] + 1,
                ),
            )
        super().__init__(data)

    def __setitem__(  # type: ignore
        self,
        key: tuple[Any, Position | Node],
        item: tuple[Any, Position | Node],
    ) -> None:
        if not isinstance(item, tuple):
            raise ValueError(
                "The value must be a tuple that"
                " contains the value and the position"
            )
        key_value, key_position = key
        value_value, value_position = item
        if isinstance(key_position, Node):
            key_position = Position(
                FileCoordinate(
                    key_position.start_point[0] + 1,
                    key_position.start_point[1] + 1,
                ),
                FileCoordinate(
                    key_position.end_point[0] + 1,
                    key_position.end_point[1] + 1,
                ),
            )
        if isinstance(value_position, Node):
            value_position = Position(
                FileCoordinate(
                    value_position.start_point[0] + 1,
                    value_position.start_point[1] + 1,
                ),
                FileCoordinate(
                    value_position.end_point[0] + 1,
                    value_position.end_point[1] + 1,
                ),
            )
        self.position_key_index[key_value] = key_position
        self.position_value_index[key_value] = value_position
        return super().__setitem__(key_value, value_value)

    def get_value_position(self, key: str) -> Position:
        return self.position_value_index[key]

    def get_key_position(self, key: str) -> Position:
        return self.position_key_index[key]


class IndexedList(UserList):
    def __init__(self, node: Node):
        self.position_index: dict[int, Position] = {}
        data: list[tuple[Any, Position]] = []
        self.position = Position(
            FileCoordinate(node.start_point[0] + 1, node.start_point[1] + 1),
            FileCoordinate(node.end_point[0] + 1, node.end_point[1] + 1),
        )
        super().__init__(data)

    def __setitem__(  # type: ignore
        self,
        index: int,
        value: tuple[Any, Position],
    ) -> None:
        if not isinstance(value, tuple):
            raise ValueError(
                "The value must be a tuple that"
                " contains the value and the position"
            )
        self.position_index[index] = value[1]
        return super().__setitem__(index, value[0])

    def append(  # type: ignore
        self,
        item: tuple[Any, Position | Node],
    ) -> None:
        value, position = item
        if isinstance(position, Node):
            position = Position(
                FileCoordinate(
                    position.start_point[0] + 1, position.start_point[1] + 1
                ),
                FileCoordinate(
                    position.end_point[0] + 1, position.end_point[1] + 1
                ),
            )
        self.position_index[len(self.data)] = position
        return super().append(value)

    def get_position(self, index: int) -> Position:
        return self.position_index[index]


class UnexpectedNodeType(Exception):
    def __init__(
        self, node: Node | str, expected_type: str | None = None
    ) -> None:
        type_name = node.type if isinstance(node, Node) else node
        if expected_type:
            super().__init__(
                f"Unexpected node type {type_name} for {expected_type}"
            )
        else:
            super().__init__(f"Unexpected node type {type_name}")


class UnexpectedChildrenLength(Exception):
    def __init__(self, node: Node | str, expected_length: int) -> None:
        type_name = node.type if isinstance(node, Node) else node
        super().__init__(
            f"Unexpected node type {type_name} for {expected_length}"
        )


class UnexpectedNode(Exception):
    def __init__(self, node: Node | str) -> None:
        type_name = node.type if isinstance(node, Node) else node
        value = node.text.decode("utf-8") if isinstance(node, Node) else None
        if value:
            super().__init__(
                f"Unexpected node type {type_name} with value {value}"
            )
        else:
            super().__init__(f"Unexpected node type {type_name}")


def index_serializer(obj: Any) -> dict[str, Any] | list[Any]:
    if isinstance(obj, UserList):
        return list(obj)
    if isinstance(obj, UserDict):
        return dict(obj)
    raise TypeError(f"Type {type(obj)} not serializable")
