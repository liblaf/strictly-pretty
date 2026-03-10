from collections.abc import (
    Mapping,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Sequence,
)
from collections.abc import Set as AbstractSet
from typing import Unpack

import wadler_lindig as wl

from liblaf.strictly_pretty._config import StrictlyPrettyOptions, config
from liblaf.strictly_pretty._helpers import pdoc_iterable
from liblaf.strictly_pretty._helpers import pdoc_mapping as _pdoc_mapping

from ._registry import pdoc


@pdoc.register(Sequence)
def pdoc_sequence(
    obj: Sequence, **kwargs: Unpack[StrictlyPrettyOptions]
) -> wl.AbstractDoc:
    maxlen: int = config.maxtuple.from_options(kwargs)
    return pdoc_iterable(obj, begin="[", end="]", maxlen=maxlen, **kwargs)


@pdoc.register(MutableSequence)
def pdoc_mutable_sequence(
    obj: MutableSequence, **kwargs: Unpack[StrictlyPrettyOptions]
) -> wl.AbstractDoc:
    maxlen: int = config.maxlist.from_options(kwargs)
    return pdoc_iterable(obj, begin="[", end="]", maxlen=maxlen, **kwargs)


@pdoc.register(AbstractSet)
def pdoc_abstract_set(
    obj: AbstractSet, **kwargs: Unpack[StrictlyPrettyOptions]
) -> wl.AbstractDoc:
    maxlen: int = config.maxfrozenset.from_options(kwargs)
    return pdoc_iterable(obj, begin="{", end="}", maxlen=maxlen, **kwargs)


@pdoc.register(MutableSet)
def pdoc_mutable_set(
    obj: MutableSet, **kwargs: Unpack[StrictlyPrettyOptions]
) -> wl.AbstractDoc:
    maxlen: int = config.maxset.from_options(kwargs)
    return pdoc_iterable(obj, begin="{", end="}", maxlen=maxlen, **kwargs)


@pdoc.register(Mapping)
@pdoc.register(MutableMapping)
def pdoc_mapping(
    obj: Mapping, **kwargs: Unpack[StrictlyPrettyOptions]
) -> wl.AbstractDoc:
    maxlen: int = config.maxdict.from_options(kwargs)
    return _pdoc_mapping(obj, begin="{", end="}", maxlen=maxlen, **kwargs)
