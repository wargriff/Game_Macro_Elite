"""Tests iCUE sans PyQt (CI Linux sans libEGL)."""

import ast
import importlib.util
import os


def _load_icue_theme():
    root = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(root, "ui", "styles", "icue_theme.py")
    spec = importlib.util.spec_from_file_location("icue_theme", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _read_lighting_defaults():
    root = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(root, "ui", "widgets", "lighting_setup_panel.py")
    tree = ast.parse(open(path, encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "DEFAULTS":
                    return ast.literal_eval(node.value)
    raise AssertionError("DEFAULTS not found")


def test_icue_palette():
    icue = _load_icue_theme()
    assert icue.ICUE["bg_main"] == "#1a1a1a"
    assert icue.ICUE["yellow"] == "#f5c518"
    assert "border_focus" in icue.ICUE


def test_icue_styles_non_empty():
    icue = _load_icue_theme()
    assert "QPushButton#tab" in icue.ICUE_HEADER_STYLE
    assert "LightingSetupPanel" in icue.ICUE_LIGHTING_PANEL


def test_lighting_defaults_constants():
    defaults = _read_lighting_defaults()
    assert defaults["ch1_type"] == "RGB Light Strip"
    assert defaults["ch2_type"] == "LL Fan Hub"
    assert "4 Strips" in defaults["ch1_qty"]
    assert "4 Fans" in defaults["ch2_qty"]
