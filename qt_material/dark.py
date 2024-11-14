import os, sys, json

sys.path.append(os.path.dirname(__file__))
from qtsymbols import *
from gui.inputdialog import autoinitdialog
from qt_material import build_stylesheet


def tryloadconfig():
    try:
        with open(__file__ + ".json", "r", encoding="utf8") as ff:
            return json.loads(ff.read())
    except:
        return {}


def get_setting_window(parent, callback):

    config = tryloadconfig()

    def callback1():
        with open(__file__ + ".json", "w", encoding="utf8") as ff:
            ff.write(json.dumps(config))
        callback()

    autoinitdialog(
        parent,
        config,
        "qt material",
        600,
        [
            {
                "type": "combo",
                "name": "Theme name",
                "k": "theme",
                "list": [
                    "amber",
                    "blue",
                    "cyan",
                    "lightgreen",
                    "medical",
                    "pink",
                    "purple",
                    "red",
                    "teal",
                    "yellow",
                ],
            },
            {"type": "okcancel", "callback": callback1},
        ],
    )


def stylesheet():
    config = tryloadconfig().get("theme", 0)
    return build_stylesheet(
        [
            "dark_amber.xml",
            "dark_blue.xml",
            "dark_cyan.xml",
            "dark_lightgreen.xml",
            "dark_medical.xml",
            "dark_pink.xml",
            "dark_purple.xml",
            "dark_red.xml",
            "dark_teal.xml",
            "dark_yellow.xml",
        ][config],
        False,
        {},
    )
