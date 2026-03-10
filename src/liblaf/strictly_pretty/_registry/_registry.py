import functools
import sys
from collections.abc import Callable
from typing import Any, Protocol, Unpack, overload

import wadler_lindig as wl

from liblaf.strictly_pretty._config import StrictlyPrettyOptions, config
from liblaf.strictly_pretty._constants import RECURSIVE


class DocCallable[T](Protocol):
    def __call__(self, obj: T, /, **kwargs: Any) -> wl.AbstractDoc | None: ...


class StrictlyPrettyRegistry:
    dispatcher: functools._SingleDispatchCallable[wl.AbstractDoc | None]
    funcs: list[DocCallable[Any]]
    funcs_lazy: list[tuple[str, str, DocCallable[Any]]]

    def __init__(self) -> None:
        @functools.singledispatch
        def dispatcher(_obj: Any, **_kwargs) -> wl.AbstractDoc | None:
            return None

        self.dispatcher = dispatcher
        self.funcs = []
        self.funcs_lazy = []

    def __call__(
        self, obj: Any, **kwargs: Unpack[StrictlyPrettyOptions]
    ) -> wl.AbstractDoc:
        from ._repr import pdoc_repr

        seen_ids: set[int] = kwargs.get("seen_ids", set())
        if id(obj) in seen_ids:
            return RECURSIVE
        seen_ids.add(id(obj))
        respect_pdoc: bool = config.respect_pdoc.from_options(kwargs)
        if respect_pdoc and hasattr(obj, "__pdoc__"):
            result: wl.AbstractDoc | None = obj.__pdoc__(**kwargs)
            if result is not None:
                return result
        self._resolve_lazy()
        result: wl.AbstractDoc | None = self.dispatcher(obj, **kwargs)
        if result is not None:
            return result
        for func in self.funcs:
            if (result := func(obj, **kwargs)) is not None:
                return result
        return pdoc_repr(obj, **kwargs)

    @overload
    def register[C: DocCallable[Any]](self, cls: type, func: C) -> C: ...
    @overload
    def register[C: DocCallable[Any]](
        self, cls: type, func: None = None
    ) -> Callable[[C], C]: ...
    def register[C: DocCallable[Any]](
        self, cls: type, func: C | None = None
    ) -> Callable[..., Any]:
        return self.dispatcher.register(cls, func)

    @overload
    def register_lazy[C: DocCallable[Any]](
        self, module: str, name: str, func: C
    ) -> C: ...
    @overload
    def register_lazy[C: DocCallable[Any]](
        self, module: str, name: str, func: None = None
    ) -> Callable[[C], C]: ...
    def register_lazy[C: DocCallable[Any]](
        self, module: str, name: str, func: C | None = None
    ) -> Callable[..., Any]:
        if func is None:
            return functools.partial(self.register_lazy, module, name)
        self.funcs_lazy.append((module, name, func))
        return func

    def register_func(self, func: DocCallable[Any]) -> DocCallable[Any]:
        self.funcs.append(func)
        return func

    def _resolve_lazy(self) -> None:
        from . import _builtins, _collections, _fieldz, _rich_repr  # noqa: F401

        if not self.funcs_lazy:
            return
        funcs_lazy: list[tuple[str, str, DocCallable[Any]]] = []
        for module_name, name, func in self.funcs_lazy:
            if module := sys.modules.get(module_name):
                cls: type = getattr(module, name)
                self.register(cls, func)
            else:
                funcs_lazy.append((module_name, name, func))
        self.funcs_lazy = funcs_lazy


pdoc = StrictlyPrettyRegistry()
