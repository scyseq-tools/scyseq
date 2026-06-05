# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import sys

sys.path.append("../../src/")

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "scyseq"
copyright = "2023, Laurent Pezard, Jean-Luc Blanc and others"
author = "Laurent Pezard, Jean-Luc Blanc and others"
release = "0.1"


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "nbsphinx",
    "myst_parser",
    "sphinx.ext.todo",
    "sphinxcontrib.bibtex",
]

templates_path = ["_templates"]
exclude_patterns = []

bibtex_bibfiles = ["references.bib"]

nb_execution_mode = "auto"

napoleon_numpy_docstring = True
napoleon_google_docstring = False

autoclass_content = "class"  # can be "class", "init", "both"

autodoc_member_order = "bysource"

# Display todos by setting to True
todo_include_todos = False
html_show_sourcelink = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
html_logo = "_static/logo_3-200px.png"
html_favicon = "_static/logo_3-favicon.png"
