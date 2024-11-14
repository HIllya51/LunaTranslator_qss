"""Module for loading style data for Qt."""

import json
import shutil
from functools import partial

from qdarktheme import __version__, _os_appearance, _resources
from qdarktheme._template import filter
from qdarktheme._template.engine import Template
from qdarktheme._util import get_cash_root_path, get_logger

_logger = get_logger(__name__)


def _detect_system_theme(default_theme) -> str:
    import darkdetect

    system_theme = darkdetect.theme()
    if system_theme is None:
        _logger.info('failed to detect system theme, qdarktheme use "{}" theme.'.format(default_theme))
        return default_theme
    return system_theme.lower()


def _color_values(theme):
    try:
        return json.loads(_resources.colors.THEME_COLOR_VALUES[theme])
    except KeyError:
        raise ValueError('invalid argument, not a dark, light or auto: "{}"'.format(theme)) from None


def _has_primary_color(custom_colors, theme) -> bool:
    if any("primary" in color for color in custom_colors):
        return True
    custom_colors_with_theme = custom_colors.get("[{}]".format(theme))
    if custom_colors_with_theme is None:
        return False
    if not isinstance(custom_colors_with_theme, dict):
        raise ValueError(
            "invalid value for argument custom_colors, not a dict type: "
            '"{}" of "[{}]" key.'.format(custom_colors_with_theme, theme)
        )
    return any("primary" in color for color in custom_colors_with_theme)


def _apply_os_accent_color(
    custom_colors, theme
):
    accent = _os_appearance.accent()
    if accent is None:
        return custom_colors
    try:
        accent_color = _resources.colors.ACCENT_COLORS[theme].get(accent)
    except KeyError:
        raise ValueError('invalid argument, not a dark, light or auto: "{}"'.format(theme)) from None
    if accent_color is None:
        return custom_colors

    if custom_colors is None:
        return {"primary": accent_color}
    custom_colors = custom_colors.copy()
    if not _has_primary_color(custom_colors, theme):
        custom_colors["primary"] = accent_color
    return custom_colors


def _mix_theme_colors(custom_colors, theme):
    colors = {id: color for id, color in custom_colors.items() if isinstance(color, str)}
    custom_colors_with_theme = custom_colors.get("[{}]".format(theme))
    if isinstance(custom_colors_with_theme, dict):
        colors.update(custom_colors_with_theme)
    elif isinstance(custom_colors_with_theme, str):
        raise ValueError(
            "invalid value for argument custom_colors, not a dict type: "
            '"{}" of "[{}]" key.'.format(custom_colors_with_theme, theme)
        )
    return colors


def _marge_colors(
    color_values, custom_colors, theme
):
    for color_id, color in _mix_theme_colors(custom_colors, theme).items():
        try:
            parent_key, *child_keys = color_id.split(">")
            color_value = color_values[parent_key]
            if len(child_keys) > 1 or (isinstance(color_value, str) and len(child_keys) != 0):
                raise KeyError

            if isinstance(color_value, str):
                color_values[parent_key] = color
            else:
                child_key = "base" if len(child_keys) == 0 else child_keys[0]
                color_value[child_key]  # Check if child_key exists.
                color_value[child_key] = color
        except KeyError:
            raise KeyError('invalid color id for argument custom_colors: "{}".'.format(color_id)) from None


def load_stylesheet(
    theme = "dark",
    corner_shape = "rounded",
    custom_colors = None,
    default_theme = "dark",
) -> str:
    """Load the style sheet which looks like flat design. There are `dark` and `light` theme.

    Args:
        theme: The theme name. There are `dark`, `light` and `auto`.
            If ``auto``, try to detect your OS's theme and accent (accent is only on Mac).
            If failed to detect OS's theme, use the default theme set in argument ``default_theme``.
            When primary color(``primary``) or primary child colors
            (such as ``primary>selection.background``) are set to custom_colors,
            disable to detect the accent.
        corner_shape: The corner shape. There are `rounded` and `sharp` shape.
        custom_colors: The custom color map. Overrides the default color for color id you set.
            Also you can customize a specific theme only. See example 6.
        default_theme: The default theme name.
            The theme set by this argument will be used when system theme detection fails.

    Raises:
        ValueError: If the arguments of this method is wrong.
        KeyError: If the color id of custom_colors is wrong.

    Returns:
        The stylesheet string for the given arguments.

    Examples:
        Set stylesheet to your Qt application.

        1. Dark Theme ::

            app = QApplication([])
            app.setStyleSheet(qdarktheme.load_stylesheet())
            # or
            app.setStyleSheet(qdarktheme.load_stylesheet("dark"))

        2. Light Theme ::

            app = QApplication([])
            app.setStyleSheet(qdarktheme.load_stylesheet("light"))

        3. Automatic detection of system theme ::

            app = QApplication([])
            app.setStyleSheet(qdarktheme.load_stylesheet("auto"))

        4. Sharp corner ::

            # Change corner shape to sharp.
            app = QApplication([])
            app.setStyleSheet(qdarktheme.load_stylesheet(corner_shape="sharp"))

        5. Customize color ::

            app = QApplication([])
            app.setStyleSheet(qdarktheme.load_stylesheet(custom_colors={"primary": "#D0BCFF"}))

        6. Customize a specific theme only ::

            app = QApplication([])
            app.setStyleSheet(
                qdarktheme.load_stylesheet(
                    theme="auto",
                    custom_colors={
                        "[dark]": {
                            "primary": "#D0BCFF",
                        }
                    },
                )
            )
    """
    if theme == "auto":
        theme = _detect_system_theme(default_theme)
        custom_colors = _apply_os_accent_color(custom_colors, theme)
    color_values = _color_values(theme)
    if corner_shape not in ("rounded", "sharp"):
        raise ValueError('invalid argument, not a rounded or sharp: "{}"'.format(corner_shape))

    if custom_colors is not None:
        _marge_colors(color_values, custom_colors, theme)
    try:
        get_cash_root_path(__version__).mkdir(parents=True, exist_ok=True)
    except:
        pass

    stylesheet = _resources.stylesheets.TEMPLATE_STYLESHEET
    try:
        from qdarktheme.qtpy.QtCore import QCoreApplication

        app = QCoreApplication.instance()
        if app is not None and not app.property("_qdarktheme_use_setup_style"):
            stylesheet += _resources.stylesheets.TEMPLATE_STANDARD_ICONS_STYLESHEET
    except Exception:  # noqa: PIE786
        pass

    # Build stylesheet
    template = Template(
        stylesheet,
        {"color": filter.color, "corner": filter.corner, "env": filter.env, "url": filter.url},
    )
    replacements = dict(color_values, **{"corner-shape": corner_shape})
    return template.render(replacements)


def clear_cache() -> None:
    """Clear the caches in system home path.

    PyQtDarkTheme build the caches of resources in the system home path.
    You can clear the caches by running this method.
    """
    try:
        cache_path = get_cash_root_path(__version__)
        shutil.rmtree(cache_path)
        _logger.info("The caches({}) has been deleted".format(cache_path))
    except FileNotFoundError:
        _logger.info("There is no caches")


def load_palette(
    theme = "dark",
    custom_colors = None,
    default_theme = "dark",
    for_stylesheet: bool = False,
):
    """Load the QPalette for the dark or light theme.

    Args:
        theme: The theme name. There are `dark`, `light` and `auto`.
            If ``auto``, try to detect system theme.
            If failed to detect system theme, use the theme set in argument ``default_theme``.
        custom_colors: The custom color map. Overrides the default color for color id you set.
            Also you can customize a specific theme only. See example 5.
        default_theme: The default theme name.
            The theme set by this argument will be used when system theme detection fails.
        for_stylesheet: If True, only includes colors that cannot be set in stylesheets, such as
            ``link`` and ``placeholder``.

    Raises:
        TypeError: If the arg name of theme is wrong.
        KeyError: If the color id of custom_colors is wrong.

    Returns:
        QPalette: The QPalette for the given theme.

    Examples:
        Set QPalette to your Qt application.

        1. Dark Theme ::

            app = QApplication([])
            app.setPalette(qdarktheme.load_palette())
            # or
            app.setPalette(qdarktheme.load_palette("dark"))

        2. Light Theme ::

            app = QApplication([])
            app.setPalette(qdarktheme.load_palette("light"))

        3. Automatic detection of system theme ::

            app = QApplication([])
            app.setPalette(qdarktheme.load_palette("auto"))

        4. Customize color ::

            app = QApplication([])
            app.setPalette(custom_colors={"primary": "#D0BCFF"})

        5. Customize a specific theme only ::

            app = QApplication([])
            app.setStyleSheet(
                qdarktheme.load_stylesheet(
                    theme="auto",
                    custom_colors={
                        "[dark]": {
                            "primary": "#D0BCFF",
                        }
                    },
                )
            )
    """
    if theme == "auto":
        theme = _detect_system_theme(default_theme)
    color_values = _color_values(theme)
    if custom_colors is not None:
        _marge_colors(color_values, custom_colors, theme)

    mk_template = partial(Template, filters={"color": filter.color, "palette": filter.palette_format})
    return _resources.palette.q_palette(mk_template, color_values, for_stylesheet)


def get_themes():
    """Return available theme names.

    Returns:
        Tuple of available theme names.
    """
    return _resources.THEMES
