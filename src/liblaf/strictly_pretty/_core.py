import enum

import wadler_lindig as wl
import wcwidth


class Mode(enum.Enum):
    BREAK = enum.auto()
    FLAT = enum.auto()


def fits(doc: wl.AbstractDoc, w: int) -> bool:
    stack: list[wl.AbstractDoc] = [doc]
    while stack and w >= 0:
        match doc := stack.pop():
            case wl.ConcatDoc(children):
                stack.extend(reversed(children))
            case wl.NestDoc(child, _indent):
                stack.append(child)
            case wl.TextDoc(text):
                if "\n" in text:
                    return False
                w -= wcwidth.width(text)
            case wl.BreakDoc(text):
                w -= wcwidth.width(text)
            case wl.GroupDoc(child):
                stack.append(child)
            case _:
                raise TypeError(type(doc))
    return w >= 0


def pdoc_format(doc: wl.AbstractDoc, w: int) -> str:
    stack: list[tuple[int, Mode, wl.AbstractDoc]] = [(0, Mode.FLAT, doc)]
    outputs: list[str] = []
    k: int = 0
    while stack:
        i, m, doc = stack.pop()
        match doc:
            case wl.ConcatDoc(children):
                stack.extend((i, m, c) for c in reversed(children))
            case wl.NestDoc(text, j):
                stack.append((i + j, m, text))
            case wl.TextDoc(text):
                outputs.append(text.replace("\n", "\n" + " " * i))
                k += wcwidth.width(text.splitlines()[-1])
            case wl.BreakDoc(text):
                match m:
                    case Mode.FLAT:
                        outputs.append(text)
                        k += wcwidth.width(text)
                    case Mode.BREAK:
                        outputs.append("\n" + " " * i)
                        k = wcwidth.width(" " * i)
                    case _:
                        raise ValueError(m)
            case wl.GroupDoc(child):
                if fits(child, w - k):
                    stack.append((i, Mode.FLAT, child))
                else:
                    stack.append((i, Mode.BREAK, child))
            case _:
                raise TypeError(type(doc))
    return "".join(outputs)
