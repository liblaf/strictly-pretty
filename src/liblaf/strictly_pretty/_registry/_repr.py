import reprlib
from typing import Any, Unpack

import wadler_lindig as wl

from liblaf.strictly_pretty._config import StrictlyPrettyOptions, config

from ._registry import pdoc


def new_repr(**kwargs: Unpack[StrictlyPrettyOptions]) -> reprlib.Repr:
    maxstring: int = config.maxstring.from_options(kwargs)
    maxother: int = config.maxother.from_options(kwargs)
    maxlevel: int = config.maxlevel.from_options(kwargs)
    maxtuple: int = config.maxtuple.from_options(kwargs)
    maxlist: int = config.maxlist.from_options(kwargs)
    maxarray: int = config.maxarray.from_options(kwargs)
    maxdict: int = config.maxdict.from_options(kwargs)
    maxset: int = config.maxset.from_options(kwargs)
    maxfrozenset: int = config.maxfrozenset.from_options(kwargs)
    maxdeque: int = config.maxdeque.from_options(kwargs)
    fillvalue: str = config.fillvalue.from_options(kwargs)
    indent: int = config.indent.from_options(kwargs)
    return reprlib.Repr(
        maxlevel=maxlevel,
        maxtuple=maxtuple,
        maxlist=maxlist,
        maxarray=maxarray,
        maxdict=maxdict,
        maxset=maxset,
        maxfrozenset=maxfrozenset,
        maxdeque=maxdeque,
        maxstring=maxstring,
        maxlong=maxother,
        maxother=maxother,
        fillvalue=fillvalue,
        indent=indent,
    )


@pdoc.register(bytearray)
@pdoc.register(bytes)
@pdoc.register(memoryview)
@pdoc.register(range)
@pdoc.register(slice)
@pdoc.register(str)
def pdoc_repr(obj: Any, **kwargs: Unpack[StrictlyPrettyOptions]) -> wl.AbstractDoc:
    return wl.TextDoc(new_repr(**kwargs).repr(obj))
