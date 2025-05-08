# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'scyseq'
copyright = '2023, Laurent Pezard, Jean-Luc Blanc and others'
author = 'Laurent Pezard, Jean-Luc Blanc and others'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import sys
sys.path.append('../../src/')
#import os
#import sys
#sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "src")))

extensions = ['sphinx.ext.autodoc', 
              'nbsphinx',
              'sphinx.ext.todo',
              'sphinxcontrib.bibtex' ]

templates_path = ['_templates']
exclude_patterns = []

bibtex_bibfiles = ['references.bib']

nb_execution_mode = 'auto'

# Display todos by setting to True
todo_include_todos = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
