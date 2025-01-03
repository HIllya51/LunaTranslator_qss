import os
import sys
import json
from collections import OrderedDict

sys.path.append(os.path.dirname(__file__))
import qdarktheme
from gui.inputdialog import autoinitdialog

theme = "dark"


def tryloadconfig():
    try:
        with open("userconfig/PyQtDarkTheme.json", "r", encoding="utf8") as ff:
            return json.loads(ff.read())
    except:
        return {}


ACCENT_COLORS = {
    "dark": OrderedDict(
        [
            ("blue", "#8ab4f7"),
            ("graphite", "#898a8f"),
            ("green", "#4caf50"),
            ("orange", "#ff9800"),
            ("pink", "#c7457f"),
            ("purple", "#af52bf"),
            ("red", "#f6685e"),
            ("yellow", "#ffeb3b"),
        ]
    ),
    "light": OrderedDict(
        [
            ("blue", "#1a73e8"),
            ("graphite", "#898a8f"),
            ("green", "#4caf50"),
            ("orange", "#ff9800"),
            ("pink", "#c7457f"),
            ("purple", "#9c27b0"),
            ("red", "#f44336"),
            ("yellow", "#f4c65f"),
        ]
    ),
}


def get_setting_window(parent, callback):

    config = tryloadconfig()

    def callback1():
        with open("userconfig/PyQtDarkTheme.json", "w", encoding="utf8") as ff:
            ff.write(json.dumps(config))
        callback()

    autoinitdialog(
        parent,
        config,
        "PyQtDarkTheme",
        600,
        [
            {
                "type": "combo",
                "name": "corner shape",
                "k": "corner_shape",
                "list": ["rounded", "sharp"],
            },
            {
                "type": "combo",
                "name": "color",
                "k": "color",
                "list": list(ACCENT_COLORS[theme].keys()),
            },
            {"type": "okcancel", "callback": callback1},
        ],
    )


def stylesheet():
    config = tryloadconfig()
    corner_shape = config.get("corner_shape", 0)
    color = config.get("color", 0)
    return qdarktheme.load_stylesheet(
        theme=theme,
        corner_shape=["rounded", "sharp"][corner_shape],
        custom_colors={"primary": list(ACCENT_COLORS[theme].values())[color]},
    )
