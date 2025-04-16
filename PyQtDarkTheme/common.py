import json
from collections import OrderedDict
import sys, os

sys.path.append(os.path.dirname(__file__))
import qdarktheme


def tryloadconfig():
    try:
        with open("userconfig/PyQtDarkTheme.json", "r", encoding="utf8") as ff:
            return json.loads(ff.read())
    except:
        return {}


ACCENT_COLORS = {
    "dark": OrderedDict(
        [
            ("pink", "#c7457f"),
            ("blue", "#8ab4f7"),
            ("graphite", "#898a8f"),
            ("green", "#4caf50"),
            ("orange", "#ff9800"),
            ("purple", "#af52bf"),
            ("red", "#f6685e"),
            ("yellow", "#ffeb3b"),
        ]
    ),
    "light": OrderedDict(
        [
            ("pink", "#c7457f"),
            ("blue", "#1a73e8"),
            ("graphite", "#898a8f"),
            ("green", "#4caf50"),
            ("orange", "#ff9800"),
            ("purple", "#9c27b0"),
            ("red", "#f44336"),
            ("yellow", "#f4c65f"),
        ]
    ),
}


def stylesheet_1(theme):
    config = tryloadconfig()
    corner_shape = config.get("corner_shape_1", "sharp")
    color = config.get("color_1", "pink")
    return qdarktheme.load_stylesheet(
        theme=theme,
        corner_shape=corner_shape,
        custom_colors={"primary": ACCENT_COLORS[theme][color]},
    )
