from __future__ import annotations

from datetime import date
from pathlib import Path
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

project_metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]

project = "Aurora Origin SDK"
author = "Aurora Development"
copyright = f"{date.today().year}, Aurora Energy Research"
release = project_metadata["version"]
version = release

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
exclude_patterns = ["_build", "_apidoc"]

autosummary_generate = True
autodoc_typehints = "signature"
autodoc_mock_imports = ["pandas"]
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
autosummary_imported_members = False
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
