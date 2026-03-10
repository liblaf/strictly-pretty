from typing import Any, Unpack

from ._config import StrictlyPrettyOptions, config
from ._core import pdoc_format
from ._registry import pdoc


def pformat(obj: Any, **kwargs: Unpack[StrictlyPrettyOptions]) -> str:
    width: int = config.width.from_options(kwargs)
    return pdoc_format(pdoc(obj, **kwargs), width)
