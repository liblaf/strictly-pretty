import pytest
import wadler_lindig as wl

from liblaf.strictly_pretty import BREAK, pdoc_format


@pytest.fixture(scope="package")
def doc() -> wl.AbstractDoc:
    return wl.GroupDoc(
        wl.TextDoc("[begin")
        + wl.NestDoc(
            BREAK
            + wl.GroupDoc(
                wl.TextDoc("[stmt;")
                + BREAK
                + wl.TextDoc("stmt;")
                + BREAK
                + wl.TextDoc("stmt;]")
            ),
            3,
        )
        + BREAK
        + wl.TextDoc("end]")
    )


def test_lindig_w50(doc: wl.AbstractDoc) -> None:
    assert pdoc_format(doc, 50) == "[begin [stmt; stmt; stmt;] end]"


def test_lindig_w30(doc: wl.AbstractDoc) -> None:
    assert (
        pdoc_format(doc, 30)
        == """[begin
   [stmt; stmt; stmt;]
end]"""
    )


def test_lindig_w10(doc: wl.AbstractDoc) -> None:
    assert (
        pdoc_format(doc, 10)
        == """[begin
   [stmt;
   stmt;
   stmt;]
end]"""
    )
