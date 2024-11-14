"""A module containing multiple filters used by template engine."""

import platform

from qdarktheme import __version__
from qdarktheme._color import Color
from qdarktheme._icon.svg import Svg
from qdarktheme._util import analyze_version_str, get_cash_root_path, get_logger
from qdarktheme.qtpy import __version__ as qt_version
from qdarktheme.qtpy.qt_compat import QT_API

_logger = get_logger(__name__)

if qt_version is None:
    _logger.warning("Failed to detect Qt version. Load Qt version as the latest version.")
    _QT_VERSION = "10.0.0"  # Fairly future version for always setting latest version.
else:
    _QT_VERSION = qt_version

if QT_API is None:
    _QT_API = "PySide6"
    _logger.warning("Failed to detect Qt binding. Load Qt API as '{}'.".format(_QT_API))
else:
    _QT_API = QT_API

if None in (qt_version, QT_API):
    _logger.warning(
        "Maybe you need to install qt-binding. "
        "Available Qt-binding packages: PySide6, PyQt6, PyQt5, PySide2."
    )


def _transform(color, color_state) -> Color:
    if color_state.get("transparent"):
        color = color.transparent(color_state["transparent"])
    if color_state.get("darken"):
        color = color.darken(color_state["darken"])
    if color_state.get("lighten"):
        return color.lighten(color_state["lighten"])
    return color


def color(color_info, state = None) -> Color:
    """Filter for template engine. This filter convert color info data to color object."""
    if isinstance(color_info, str):
        return Color.from_hex(color_info)

    base_color_format = color_info["base"]  # type: ignore
    color = Color.from_hex(base_color_format)

    if state is None:
        return color

    transforms = color_info[state]
    return Color.from_hex(transforms) if isinstance(transforms, str) else _transform(color, transforms)


def palette_format(color: Color) -> str:
    """Filter for template engine. This filter convert color object to ARGB hex format.

    QPalette parser for hex only support ARGB hex format. color.Color class use RGB hex format.
    So we need to convert Color object to ARGB hex format.
    """
    return "#{}".format(color.to_hex_argb())


def url(color: Color, id, rotate: int = 0) -> str:
    """Filter for template engine. This filter create url for svg and output svg file."""
    svg_path = get_cash_root_path(__version__) / "{}_{}_{}.svg".format(id, color._to_hex(), rotate)
    url = "url({})".format(svg_path.as_posix())
    if svg_path.exists():
        return url
    svg = Svg(id).colored(color).rotate(rotate)
    try:
        svg_path.write_text(str(svg))
    except:
        import os
        os.makedirs(os.path.dirname(str(svg_path)), exist_ok=True)
        with open(str(svg_path), 'w') as ff:
            ff.write(str(svg))
    return url


def env(
    text, value, version = None, qt = None, os = None
) -> str:
    """Filter for template engine. This filter output empty string when unexpected environment."""
    if version and not analyze_version_str(_QT_VERSION, version):
        return ""
    if qt and qt.lower() != _QT_API.lower():
        return ""
    if os and platform.system().lower() not in os.lower():
        return ""
    return value.replace("${}", str(text))


def corner(corner_shape, size) -> str:
    """Filter for template engine. This filter manage corner shape."""
    return size if corner_shape == "rounded" else "0"
