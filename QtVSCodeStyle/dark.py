import os, sys, json

sys.path.append(os.path.dirname(__file__))
import qtvscodestyle as qtvsc
from qtsymbols import *
from gui.inputdialog import autoinitdialog


def tryloadconfig():
    try:
        with open("userconfig/QtVSCodeStyle_d.json", "r", encoding="utf8") as ff:
            return json.loads(ff.read())
    except:
        return {}


def get_setting_window(parent, callback):

    config = tryloadconfig()

    def callback1():
        with open("userconfig/QtVSCodeStyle_d.json", "w", encoding="utf8") as ff:
            ff.write(json.dumps(config))
        callback()

    autoinitdialog(
        parent,
        config,
        "QtVSCodeStyle",
        600,
        [
            {
                "type": "combo",
                "name": "Theme name",
                "k": "theme",
                "list": [
                    "Abyss",
                    "Dark (Visual Studio)",
                    "Kimbie Dark",
                    "Monokai",
                    "Monokai Dimmed",
                    "Red",
                    "Solarized Dark",
                    "Tomorrow Night Blue",
                    "Dark High Contrast",
                ],
            },
            {"type": "okcancel", "callback": callback1},
        ],
    )


def stylesheet():
    config = tryloadconfig().get("theme", 0)

    return qtvsc.load_stylesheet(
        [
            qtvsc.Theme.ABYSS,
            qtvsc.Theme.DARK_VS,
            qtvsc.Theme.KIMBIE_DARK,
            qtvsc.Theme.MONOKAI,
            qtvsc.Theme.MONOKAI_DIMMED,
            qtvsc.Theme.RED,
            qtvsc.Theme.SOLARIZED_DARK,
            qtvsc.Theme.TOMORROW_NIGHT_BLUE,
            qtvsc.Theme.DARK_HIGH_CONTRAST,
        ][config]
    )
