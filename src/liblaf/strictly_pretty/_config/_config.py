import contextlib
import contextvars
from collections.abc import Generator
from typing import Self, TypedDict, Unpack

import wadler_lindig as wl

from ._fields import BoolField, ConfigField, IntField, StrField


class StrictlyPrettyOptions(TypedDict, total=False):
    maxlevel: int
    maxtuple: int
    maxlist: int
    maxarray: int
    maxdict: int
    maxset: int
    maxfrozenset: int
    maxdeque: int
    maxstring: int
    maxlong: int
    maxother: int
    fillvalue: wl.AbstractDoc | str
    indent: int

    width: int | None
    hide_defaults: bool
    show_type_module: bool
    show_dataclass_module: bool
    show_function_module: bool
    respect_pdoc: bool

    seen_ids: set[int]


class StrictlyPrettyConfig:
    # ref: <https://docs.python.org/3/library/reprlib.html>
    maxlevel: IntField = IntField("maxlevel", 6)
    maxtuple: IntField = IntField("maxtuple", 6)
    maxlist: IntField = IntField("maxlist", 6)
    maxarray: IntField = IntField("maxarray", 6)
    maxdict: IntField = IntField("maxdict", 6)
    maxset: IntField = IntField("maxset", 6)
    maxfrozenset: IntField = IntField("maxfrozenset", 6)
    maxdeque: IntField = IntField("maxdeque", 6)
    maxstring: IntField = IntField("maxstring", 30)
    maxlong: IntField = IntField("maxlong", 30)
    maxother: IntField = IntField("maxother", 30)
    fillvalue: StrField = StrField("fillvalue", "…")
    indent: IntField = IntField("indent", 2)

    # ref: <https://docs.kidger.site/wadler_lindig/api/>
    width: IntField = IntField("width", 88)
    hide_defaults: BoolField = BoolField("hide_defaults", True)  # noqa: FBT003
    show_type_module: BoolField = BoolField("show_type_module", True)  # noqa: FBT003
    show_dataclass_module: BoolField = BoolField("show_dataclass_module", False)  # noqa: FBT003
    show_function_module: BoolField = BoolField("show_function_module", False)  # noqa: FBT003
    respect_pdoc: BoolField = BoolField("respect_pdoc", True)  # noqa: FBT003

    @contextlib.contextmanager
    def override(self, **kwargs: Unpack[StrictlyPrettyOptions]) -> Generator[Self]:
        tokens: dict[ConfigField, contextvars.Token] = {}
        for name, value in kwargs.items():
            field: ConfigField = getattr(self, name)
            tokens[field] = field.var.set(value)
        try:
            yield self
        finally:
            for field, token in tokens.items():
                field.var.reset(token)


config = StrictlyPrettyConfig()
