import wadler_lindig as wl

BREAK: wl.BreakDoc = wl.BreakDoc(" ")
COLON: wl.AbstractDoc = wl.TextDoc(": ")
COMMA: wl.AbstractDoc = wl.TextDoc(",") + BREAK
EQUAL: wl.AbstractDoc = wl.TextDoc("=")
RECURSIVE: wl.AbstractDoc = wl.TextDoc("<recursive>")
