from typing import NamedTuple

import numpy as np

import liblaf.strictly_pretty as sp


def test_list() -> None:
    assert sp.pformat([1, 2]) == ("[1, 2]")
    assert sp.pformat([1]) == "[1]"
    assert sp.pformat([]) == "[]"


def test_tuple() -> None:
    assert sp.pformat((1, 2)) == "(1, 2)"
    assert sp.pformat((1,)) == "(1,)"
    assert sp.pformat(()) == "()"


def test_dict() -> None:
    assert sp.pformat({"a": 1, "b": 2}) == "{'a': 1, 'b': 2}"
    assert sp.pformat({"a": 1}) == "{'a': 1}"
    assert sp.pformat({}) == "{}"


def test_named_tuple() -> None:
    class M(NamedTuple):
        a: int

    assert sp.pformat(M(1)) == "M(a=1)"


def test_numpy_array() -> None:
    assert sp.pformat(np.array(1)) == "i64[](numpy)"
    assert sp.pformat(np.arange(12).reshape(3, 4)) == "i64[3,4](numpy)"
    assert sp.pformat(np.array(1), short_arrays=False) == "array(1)"


def test_builtins() -> None:
    assert sp.pformat(1) == "1"
    assert sp.pformat(0.1) == "0.1"
    assert sp.pformat(True) == "True"  # noqa: FBT003
    assert sp.pformat(1 + 1j) == "(1+1j)"
    assert sp.pformat("hi") == "'hi'"
