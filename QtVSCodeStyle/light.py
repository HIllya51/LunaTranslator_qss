import os, sys, json

sys.path.append(os.path.dirname(__file__))
import qtvscodestyle as qtvsc
from qtsymbols import *
from gui.inputdialog import autoinitdialog


def tryloadconfig():
    try:
        with open("userconfig/QtVSCodeStyle_l.json", "r", encoding="utf8") as ff:
            return json.loads(ff.read())
    except:
        return {}


def get_setting_window(parent, callback):

    config = tryloadconfig()

    def callback1():
        with open("userconfig/QtVSCodeStyle_l.json", "w", encoding="utf8") as ff:
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
                "list": ["Light (Visual Studio)", "Quiet Light", "Solarized Light"],
            },
            {"type": "okcancel", "callback": callback1},
        ],
    )


def stylesheet():
    config = tryloadconfig().get("theme", 0)

    return qtvsc.load_stylesheet(
        [qtvsc.Theme.LIGHT_VS, qtvsc.Theme.QUIET_LIGHT, qtvsc.Theme.SOLARIZED_LIGHT][
            config
        ]
    )
