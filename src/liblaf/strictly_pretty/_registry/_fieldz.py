from collections.abc import Sequence
from typing import Any, Unpack

import fieldz
import wadler_lindig as wl

from liblaf.strictly_pretty._config import StrictlyPrettyOptions, config
from liblaf.strictly_pretty._helpers import pdoc_dataclass

from ._registry import pdoc


@pdoc.register_func
def pdoc_fieldz(
    obj: Any, **kwargs: Unpack[StrictlyPrettyOptions]
) -> wl.AbstractDoc | None:
    try:
        fields: Sequence[fieldz.Field] = fieldz.fields(obj)
    except TypeError:
        return None
    hide_defaults: bool = config.hide_defaults.from_options(kwargs)
    pairs: list[tuple[str, Any]] = []
    for field in fields:
        if not field.repr:
            continue
        value: Any = getattr(obj, field.name, field.MISSING)
        if hide_defaults and value is field.default:
            continue
        pairs.append((field.name, value))
    return pdoc_dataclass(obj, pairs, **kwargs)
