import itertools
from collections.abc import Callable, Iterable, Iterator, Mapping
from typing import Any, Unpack

import wadler_lindig as wl

from liblaf.strictly_pretty._config import StrictlyPrettyOptions, config
from liblaf.strictly_pretty._constants import COLON, COMMA, EQUAL
from liblaf.strictly_pretty._registry import pdoc

type DocLike = wl.AbstractDoc | str


def as_doc(doc: DocLike) -> wl.AbstractDoc:
    if isinstance(doc, str):
        return wl.TextDoc(doc)
    return doc


def bracketed(
    begin: DocLike, docs: Iterable[DocLike], sep: DocLike, end: DocLike, indent: int
) -> wl.AbstractDoc:
    begin: wl.AbstractDoc = as_doc(begin)
    docs: list[wl.AbstractDoc] = [as_doc(doc) for doc in docs]
    sep: wl.AbstractDoc = as_doc(sep)
    end: wl.AbstractDoc = as_doc(end)
    return wl.bracketed(begin, docs, sep, end, indent)


def join(sep: DocLike, docs: Iterable[DocLike]) -> wl.AbstractDoc:
    sep: wl.AbstractDoc = as_doc(sep)
    docs: list[wl.AbstractDoc] = [as_doc(doc) for doc in docs]
    return wl.join(sep, docs)


def named_objs(
    pairs: Iterable[tuple[str | None, Any]], **kwargs: Unpack[StrictlyPrettyOptions]
) -> list[wl.AbstractDoc]:
    def func(item: tuple[str | None, Any], **kwargs) -> wl.AbstractDoc:
        name, value = item
        if not name:
            return pdoc(value, **kwargs)
        return wl.TextDoc(name) + EQUAL + pdoc(value, **kwargs)

    return map_with_maxlen(func, pairs, **kwargs)


def map_with_maxlen(
    func: Callable[..., wl.AbstractDoc],
    iterable: Iterable[Any],
    maxlen: int | None = None,
    **kwargs,
) -> list[wl.AbstractDoc]:
    if maxlen is None:
        return [func(item, **kwargs) for item in iterable]
    it: Iterator[Any] = iter(iterable)
    docs: list[wl.AbstractDoc] = [
        func(item, **kwargs) for item in itertools.islice(it, maxlen)
    ]
    try:
        next(it)
    except StopIteration:
        return docs
    fillvalue: str = config.fillvalue.from_options(kwargs)
    fillvalue: wl.AbstractDoc = as_doc(fillvalue)
    docs.append(fillvalue)
    return docs


def pdoc_dataclass_type(
    cls: type, **kwargs: Unpack[StrictlyPrettyOptions]
) -> wl.AbstractDoc:
    kwargs["show_type_module"] = config.show_dataclass_module.from_options(kwargs)
    return pdoc(cls, **kwargs)


def pdoc_dataclass(
    obj: Any,
    fields: Iterable[tuple[str | None, Any]],
    *,
    begin: DocLike = "(",
    end: DocLike = ")",
    show_type: bool = True,
    **kwargs: Unpack[StrictlyPrettyOptions],
) -> wl.AbstractDoc:
    indent: int = config.indent.from_options(kwargs)
    maxlevel: int = config.maxlevel.from_options(kwargs)
    kwargs["maxlevel"] = maxlevel - 1
    if show_type:
        pdoc_cls: wl.AbstractDoc = pdoc_dataclass_type(type(obj), **kwargs)
        begin: wl.AbstractDoc = pdoc_cls + as_doc(begin)
    docs: list[wl.AbstractDoc] = named_objs(fields, **kwargs)
    return bracketed(begin=begin, docs=docs, sep=COMMA, end=end, indent=indent)


def pdoc_iterable(
    obj: Iterable[Any],
    *,
    append_comma_if_single: bool = False,
    begin: DocLike = "[",
    end: DocLike = "]",
    maxlen: int | None = None,
    show_type: bool = True,
    **kwargs: Unpack[StrictlyPrettyOptions],
) -> wl.AbstractDoc:
    maxlen: int = config.maxlist.from_value(maxlen)
    indent: int = config.indent.from_options(kwargs)
    maxlevel: int = config.maxlevel.from_options(kwargs)
    kwargs["maxlevel"] = maxlevel - 1
    if show_type:
        pdoc_cls: wl.AbstractDoc = pdoc_dataclass_type(type(obj), **kwargs)
        begin: wl.AbstractDoc = pdoc_cls + as_doc(begin)
    docs: list[wl.AbstractDoc] = map_with_maxlen(pdoc, obj, maxlen=maxlen, **kwargs)
    if append_comma_if_single and len(docs) == 1:
        docs[0] = docs[0] + wl.TextDoc(",")
    return bracketed(begin=begin, docs=docs, sep=COMMA, end=as_doc(end), indent=indent)


def pdoc_mapping(
    obj: Mapping[Any, Any],
    *,
    begin: DocLike = "{",
    end: DocLike = "}",
    maxlen: int | None = None,
    show_type: bool = True,
    **kwargs: Unpack[StrictlyPrettyOptions],
) -> wl.AbstractDoc:
    maxlen: int = config.maxdict.from_value(maxlen)
    indent: int = config.indent.from_options(kwargs)
    maxlevel: int = config.maxlevel.from_options(kwargs)
    kwargs["maxlevel"] = maxlevel - 1
    if show_type:
        pdoc_cls: wl.AbstractDoc = pdoc_dataclass_type(type(obj), **kwargs)
        begin: wl.AbstractDoc = pdoc_cls + as_doc(begin)

    def func(item: tuple[Any, Any], **kwargs) -> wl.AbstractDoc:
        key, value = item
        return pdoc(key, **kwargs) + COLON + pdoc(value, **kwargs)

    docs: list[wl.AbstractDoc] = map_with_maxlen(
        func, obj.items(), maxlen=maxlen, **kwargs
    )
    return bracketed(begin=begin, docs=docs, sep=COMMA, end=end, indent=indent)
