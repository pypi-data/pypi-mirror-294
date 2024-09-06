from importlib import import_module
from typing import Any


def import_member(member_str: str) -> tuple[Any, tuple[str, str]]:
    module_name, member_name = member_str.rsplit(":", 1)
    module = import_module(module_name)
    obj: object | None = getattr(module, member_name, None)
    return obj, (member_name, module_name)
