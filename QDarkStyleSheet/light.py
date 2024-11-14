import os


def stylesheet():
    from . import lightstyle_rc

    with open(
        os.path.join(os.path.dirname(__file__), "light.qss"),
        "r",
        encoding="utf8",
    ) as ff:
        s = ff.read()
    return s
