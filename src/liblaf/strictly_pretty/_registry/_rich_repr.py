from typing import Any, Unpack

import wadler_lindig as wl
from rich.repr import RichReprResult

from liblaf.strictly_pretty._config import StrictlyPrettyOptions, config
from liblaf.strictly_pretty._helpers import pdoc_dataclass

from ._registry import pdoc


@pdoc.register_func
def pdoc_rich_repr(
    obj: Any, **kwargs: Unpack[StrictlyPrettyOptions]
) -> wl.AbstractDoc | None:
    if not hasattr(obj, "__rich_repr__"):
        return None
    rich_repr_result: RichReprResult | None = obj.__rich_repr__()
    if rich_repr_result is None:
        return None
    hide_defaults: bool = config.hide_defaults.from_options(kwargs)
    pairs: list[tuple[str | None, Any]] = []
    for field in rich_repr_result:
        match field:
            case (name, value, default):
                if hide_defaults and value is default:
                    continue
                pairs.append((name, value))
            case (name, value):
                pairs.append((name, value))
            case value:
                pairs.append((None, value))
    return pdoc_dataclass(obj, pairs, **kwargs)
