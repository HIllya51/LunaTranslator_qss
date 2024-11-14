import os


def stylesheet():
    from . import darkstyle_rc

    with open(
        os.path.join(os.path.dirname(__file__), "dark.qss"),
        "r",
        encoding="utf8",
    ) as ff:
        s = ff.read()
    return s
