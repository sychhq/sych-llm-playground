"""Sphinx configuration."""
project = "Sych LLM Playground"
author = "Sych Inc."
copyright = "2023, Sych Inc."
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
