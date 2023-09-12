# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import pathlib
import sys

src_path = pathlib.Path(__file__).parents[2].joinpath('src').resolve().as_posix()
sys.path.insert(0, src_path)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Better Bound Box'
copyright = '2023, Rodrigo Gama'
author = 'Rodrigo Gama'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']

# -- Autodoc ------------------------------------------------------------------

autodoc_default_flags = ['members', 'undoc-members', 'show-inheritance']
autodoc_member_order = 'bysource'

autodoc_mock_imports = ["bpy","bmesh", "mathutils"]

def autodoc_skip(app, what, name, obj, skip, options):
    '''Don't skip __init__ method for autodoc.'''
    if name == '__init__':
        return False

    return skip

# -- Setup --------------------------------------------------------------------

def setup(app):
    app.connect('autodoc-skip-member', autodoc_skip)