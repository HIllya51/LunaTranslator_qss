import os, sys, json

sys.path.append(os.path.dirname(__file__))
from qtsymbols import *
from gui.inputdialog import autoinitdialog
from qt_material import build_stylesheet


def tryloadconfig():
    try:
        with open("userconfig/qt_material_l.json", "r", encoding="utf8") as ff:
            return json.loads(ff.read())
    except:
        return {}


def get_setting_window(parent, callback):

    config = tryloadconfig()

    def callback1():
        with open("userconfig/qt_material_l.json", "w", encoding="utf8") as ff:
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
                    "blue_500",
                    "cyan",
                    "cyan_500",
                    "lightgreen",
                    "lightgreen_500",
                    "orange",
                    "pink",
                    "pink_500",
                    "purple",
                    "purple_500",
                    "red",
                    "red_500",
                    "teal",
                    "teal_500",
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
            "light_amber.xml",
            "light_blue.xml",
            "light_blue_500.xml",
            "light_cyan.xml",
            "light_cyan_500.xml",
            "light_lightgreen.xml",
            "light_lightgreen_500.xml",
            "light_orange.xml",
            "light_pink.xml",
            "light_pink_500.xml",
            "light_purple.xml",
            "light_purple_500.xml",
            "light_red.xml",
            "light_red_500.xml",
            "light_teal.xml",
            "light_teal_500.xml",
            "light_yellow.xml",
        ][config],
        False,
        {},
    )
