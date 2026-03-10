import types
from collections.abc import Mapping, Sequence
from collections.abc import Set as AbstractSet
from typing import NamedTuple, Unpack, cast

import wadler_lindig as wl

from liblaf.strictly_pretty._config import StrictlyPrettyOptions, config
from liblaf.strictly_pretty._helpers import pdoc_dataclass, pdoc_iterable, pdoc_mapping

from ._registry import pdoc


@pdoc.register(list)
def pdoc_list(obj: Sequence, **kwargs: Unpack[StrictlyPrettyOptions]) -> wl.AbstractDoc:
    maxlen: int = config.maxlist.from_options(kwargs)
    return pdoc_iterable(
        obj, begin="[", end="]", maxlen=maxlen, show_type=False, **kwargs
    )


@pdoc.register(tuple)
def pdoc_tuple(
    obj: Sequence, **kwargs: Unpack[StrictlyPrettyOptions]
) -> wl.AbstractDoc:
    if hasattr(obj, "_fields"):
        obj: NamedTuple = cast("NamedTuple", obj)
        return pdoc_named_tuple(obj, **kwargs)
    maxlen: int = config.maxtuple.from_options(kwargs)
    return pdoc_iterable(
        obj,
        append_comma_if_single=True,
        begin="(",
        end=")",
        maxlen=maxlen,
        show_type=False,
        **kwargs,
    )


def pdoc_named_tuple(
    obj: NamedTuple, **kwargs: Unpack[StrictlyPrettyOptions]
) -> wl.AbstractDoc:
    return pdoc_dataclass(
        obj, fields=[(field, getattr(obj, field)) for field in obj._fields], **kwargs
    )


@pdoc.register(set)
def pdoc_set(
    obj: AbstractSet, **kwargs: Unpack[StrictlyPrettyOptions]
) -> wl.AbstractDoc:
    maxlen: int = config.maxset.from_options(kwargs)
    return pdoc_iterable(
        obj, begin="{", end="}", maxlen=maxlen, show_type=False, **kwargs
    )


@pdoc.register(frozenset)
def pdoc_frozenset(
    obj: AbstractSet, **kwargs: Unpack[StrictlyPrettyOptions]
) -> wl.AbstractDoc:
    maxlen: int = config.maxfrozenset.from_options(kwargs)
    return pdoc_iterable(
        obj, begin="{", end="}", maxlen=maxlen, show_type=True, **kwargs
    )


@pdoc.register(dict)
def pdoc_dict(obj: Mapping, **kwargs: Unpack[StrictlyPrettyOptions]) -> wl.AbstractDoc:
    maxlen: int = config.maxdict.from_options(kwargs)
    return pdoc_mapping(
        obj, begin="{", end="}", maxlen=maxlen, show_type=False, **kwargs
    )


@pdoc.register(type)
def pdoc_type(obj: type, **kwargs: Unpack[StrictlyPrettyOptions]) -> wl.AbstractDoc:
    show_type_module: bool = config.show_type_module.from_options(kwargs)
    if not show_type_module or obj.__module__ in {
        "builtins",
        "typing",
        "typing_extensions",
        "collections.abc",
    }:
        return wl.TextDoc(obj.__name__)
    return wl.TextDoc(f"{obj.__module__}.{obj.__qualname__}")


@pdoc.register(types.NoneType)
def pdoc_none(_obj: None, **_kwargs: Unpack[StrictlyPrettyOptions]) -> wl.AbstractDoc:
    return wl.TextDoc("None")
