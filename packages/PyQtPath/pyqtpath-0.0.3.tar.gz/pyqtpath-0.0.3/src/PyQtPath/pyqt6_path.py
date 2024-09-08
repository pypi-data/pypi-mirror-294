from typing import Optional

from PyQt6.QtWidgets import QWidget


def get_nested_child(widget: QWidget, *path: type[QWidget] | int) -> Optional:
    path_list: list[type[QWidget] | int] = list(path)
    normalized_path: list[(type[QWidget], int)] = __normalize_path(path_list)
    return __nested_child(widget, normalized_path)


def __nested_child(widget: QWidget, path: list[(type[QWidget], int)]) -> Optional:
    current_widget: QWidget = widget
    for part in path:
        clazz: type[QWidget] = part[0]
        index: int = part[1]
        children: list[QWidget] = current_widget.findChildren(clazz)
        if len(children) == 0:
            return None
        current_widget = children[index]
    return current_widget


def __normalize_path(path: list[type[QWidget] | int]) -> list[(type[QWidget], int)]:
    if path is None or len(path) == 0:
        return []
    if isinstance(path[0], int):
        raise RuntimeError("The 1st element cannot be an index")
    for i, part in enumerate(path):
        if isinstance(part, int):
            continue
        next_part: type[QWidget] | int = path[i + 1] if i < len(path) - 1 else None
        if next_part is not None and isinstance(next_part, int):
            yield part, next_part
        else:
            yield part, 0
