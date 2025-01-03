import os
import sys

# Qt6
_QT_API_PYSIDE6 = "PySide6"
_QT_API_PYQT6 = "PyQt6"
# Qt5
_QT_API_PYQT5 = "PyQt5"
_QT_API_PYSIDE2 = "PySide2"
# PATH
_QT_API_ENV = os.environ.get("QT_API")
if _QT_API_ENV is not None:
    _QT_API_ENV = _QT_API_ENV.lower()

_API_LIST = [_QT_API_PYSIDE6, _QT_API_PYQT6, _QT_API_PYQT5, _QT_API_PYSIDE2]

_ENV_TO_MODULE = {
    "pyside6": _QT_API_PYSIDE6,
    "pyqt6": _QT_API_PYQT6,
    "pyqt5": _QT_API_PYQT5,
    "pyside2": _QT_API_PYSIDE2,
    None: None,
}


def _get_loaded_api() :
    """Return which API is loaded, if any
    If this returns anything besides None,
    importing any other Qt-binding is unsafe.
    Returns
    -------
    None, 'PySide6', 'PyQt6', 'PyQt5', 'PySide2'
    """
    for api in _API_LIST:
        if sys.modules.get("{}.QtCore".format(api)):
            return api
    try:
        return _ENV_TO_MODULE[_QT_API_ENV]
    except KeyError:
        raise RuntimeError(
            "The environment variable QT_API has the unrecognized value "
            "{!r}; "
            "valid values are {}".format(_QT_API_ENV, [k for k in _ENV_TO_MODULE if k is not None])
        ) from None


def _get_installed_api() :
    """Return which API is installed.

    Returns
    -------
    None, 'PySide6', 'PyQt6', 'PyQt5', 'PySide2'
    """
    # Fix [AttributeError: module 'importlib' has no attribute 'util']
    # See https://stackoverflow.com/a/39661116/13452582
    from importlib import util

    for api in _API_LIST:
        if util.find_spec(api) is not None:
            return api
    return None


QT_API = _get_loaded_api()
if QT_API is None:
    QT_API = _get_installed_api()
if QT_API is None:
    raise ImportError(
        "Failed to import qt-binding. Check modules(pip list)."
        "\nAvailable Qt-binding modules: PySide6, PyQt6, PyQt5, PySide2."
    )
