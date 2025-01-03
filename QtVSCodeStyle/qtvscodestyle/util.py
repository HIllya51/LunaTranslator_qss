

import re

from qtvscodestyle.vscode.color import Color


# https://gist.github.com/bgusach/a967e0587d6e01e889fd1d776c5f3729
def multireplace(target, replacements) -> str:
    replacements_sorted = sorted(replacements, key=len, reverse=True)
    replacements_escaped = [re.escape(i) for i in replacements_sorted]
    pattern = re.compile("|".join(replacements_escaped))
    return pattern.sub(lambda match: replacements[match.group()], target)


# QSvg does not support rgba(...). Therefore, we need to set the alpha value to `fill-opacity` instead.
def to_svg_color_format(color) -> str:
    if color is None:
        return 'fill=""'
    r, g, b, a = color.rgba
    return 'fill="rgb({}, {}, {})" fill-opacity="{}"'.format(r,g,b,a)
