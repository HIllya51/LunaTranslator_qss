

import json
import operator
import re
from distutils.version import StrictVersion
from importlib import resources
from pathlib import Path

from qtvscodestyle.util import multireplace, to_svg_color_format
from qtvscodestyle.vscode.color import Color


# A class that handle the properties of the $url{...} variable in the stylesheet template.
class _Url:
    def __init__(self,icon,id,ro,path) -> None:
        
        self.icon=icon
        self.id=id
        self.rotate=ro
        self.path=path

from collections import OrderedDict

def _parse_env_patch(stylesheet):
    try:
        from qtvscodestyle.qtpy import __version__ as qt_version
    except ImportError:
        print("Failed to load Qt version. Load stylesheet as the latest version.")
        print("-----------------------------------------------------------------")
        qt_version = "10.0.0"  # Fairly future version for always setting latest version.

    # greater_equal and less_equal must be evaluated before greater and less.
    operators = OrderedDict([("==", operator.eq),( "!=", operator.ne),(">=", operator.ge),( "<=", operator.le),( ">", operator.gt),( "<", operator.lt)])

    replacements = {}

    for match in re.finditer(r"\$env_patch\{[\s\S]*?\}", stylesheet):
        match_text = match.group()
        json_text = match_text.replace("$env_patch", "")
        property = json.loads(json_text)

        for qualifier in operators.keys():
            if qualifier in property["version"]:
                version = property["version"].replace(qualifier, "")
                break
        else:
            raise SyntaxError("invalid character in qualifier. Available qualifiers {}".format(list(operators.keys())))

        is_true = operators[qualifier](StrictVersion(qt_version), StrictVersion(version))
        replacements[match_text] = property["value"] if is_true else ""
    return replacements


def _parse_theme_type_patch(stylesheet, theme_type) :
    replacements = {}
    for match in re.finditer(r"\$type_patch\{[\s\S]*?\};", stylesheet):
        match_text = match.group().rstrip(";")
        json_text = match_text.replace("$type_patch", "")

        property = json.loads(json_text)
        theme_types = property["types"].replace(" ", "").split("|")
        value = property["value"]
        qss_text = "\n".join(value if type(value) is list else [value])
        replacements[match_text] = qss_text if theme_type in theme_types else ""
    return replacements


def _parse_url(stylesheet, dir_path, is_designer = False) :
    urls = set()
    replacements = {}
    for match in re.finditer(r"\$url\{.+\}", stylesheet):
        match_text = match.group()
        json_text = match_text.replace("$url", "")
        _=json.loads(json_text)
        icon, id, rotate = _['icon'],_['id'],_['rotate']
        file_name = "{}_{}_{}.svg".format(icon.replace('.svg', ''),id, rotate)
        urls.add(_Url(icon, id, rotate, dir_path / file_name))

        # In windows, the path is a backslash. Replase backslash to slash.
        full_path = (dir_path / file_name).as_posix()
        value = ":/vscode/{}".format(file_name) if is_designer else str(full_path)
        replacements[match_text] = "url({})".format(value)
    return replacements, urls


def _output_converted_svg_file(colors, urls) :
    svg_codes = {}  # {file name: svg code}
    for content in resources.contents("qtvscodestyle.vscode.icons"):
        if ".svg" not in content:  # Only svg file
            continue
        svg_code = resources.read_text("qtvscodestyle.vscode.icons", content)
        svg_codes[content] = svg_code

    for content in resources.contents("qtvscodestyle.stylesheet.icons"):
        if ".svg" not in content:  # Only svg file
            continue
        svg_code = resources.read_text("qtvscodestyle.stylesheet.icons", content)
        svg_codes[content] = svg_code
    for url in urls:
        color = colors["$" + url.id]
        # Change color and rotate. See https://stackoverflow.com/a/15139069/13452582
        new_contents = '{} transform="rotate({}, 8, 8)"'.format(to_svg_color_format(color), url.rotate)
        svg_code_converted = svg_codes[url.icon].replace('fill="currentColor"', new_contents)

        with url.path.open("w") as f:
            f.write(svg_code_converted)


def build_stylesheet(
    colors, theme_type, output_svg_path, is_designer
) :
    stylesheet_template = resources.read_text("qtvscodestyle.stylesheet", "template.qss")
    # Convert id for stylesheet variable
    colors = {"${}".format(id).replace(".", "_"): color for id, color in colors.items()}

    # Parse $type_patch{...} and $env_patch{...} in template stylesheet.
    type_patch_replacements = _parse_theme_type_patch(stylesheet_template, theme_type)
    env_patch_replacements = _parse_env_patch(stylesheet_template)

    # Replace value before parsing $url{...}.
    patch_replacements={}
    patch_replacements.update(type_patch_replacements)
    patch_replacements.update(env_patch_replacements)
    stylesheet_template = multireplace(stylesheet_template, patch_replacements)

    # Parse $url{...} in template stylesheet.
    url_replacements, urls = _parse_url(stylesheet_template, output_svg_path, is_designer)
    _output_converted_svg_file(colors, urls)

    # Create stylesheet
    colors_str = {id: ("" if color is None else str(color)) for id, color in colors.items()}
    replacements={}
    replacements.update(colors_str)
    replacements.update(url_replacements)
    stylesheet = multireplace(stylesheet_template, replacements)
    return stylesheet
