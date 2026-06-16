from __future__ import annotations

from datetime import date
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]

project_metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]

project = "Aurora Origin SDK"
author = "Aurora Development"
copyright = f"{date.today().year}, Aurora Energy Research"
release = project_metadata["version"]
version = release

extensions = [
    "myst_parser",
    "autodoc2",
    "sphinx.ext.githubpages",
]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
exclude_patterns = ["_build"]

# sphinx-autodoc2 statically analyses the package and renders docstrings as MyST
# Markdown, so docstrings are authored in Markdown directly -- fenced code blocks
# and inline code render natively. The `service`, `types` and `gql` subpackages
# are PEP-420 namespace packages (no __init__.py), so autodoc2 auto_mode cannot
# traverse into them; we use manual mode and curate the modules in docs/api/.
autodoc2_packages = [
    {
        "path": "../src/origin_sdk",
        "module": "origin_sdk",
        "auto_mode": False,
    },
]
autodoc2_render_plugin = "myst"
autodoc2_hidden_objects = ["dunder", "private"]
# `dict`-subclass TypedDicts (e.g. InputsDemandVariables) re-expose every inherited
# dict method, which autodoc2 reports as duplicate items. They are noise.
suppress_warnings = ["autodoc2.dup_item"]

# Enable sphinx-style field lists (:param:/:returns:/:raises:) inside Markdown
# docstrings so parameter documentation renders as a definition list.
myst_enable_extensions = ["fieldlist"]
myst_heading_anchors = 3

html_theme = "shibuya"
html_title = "Aurora Origin SDK Docs"
html_logo = "_static/logo.svg"
html_baseurl = "https://ghp.auroraer.com/aurora-origin-python-sdk/"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_theme_options = {
    "accent_color": "orange",
    "color_mode": "auto",
    "dark_code": False,
    "page_layout": "default",
}
html_sidebars = {
    "**": [
        "sidebars/localtoc.html",
    ]
}
