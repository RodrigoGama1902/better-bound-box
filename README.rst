#################
BETTER BOUND BOX - Blender Module
#################

This module provides a better BoundBox system for Blender integrations, 
with support for multiple objects and various utility functions.

If you are creating a Blender integration that will deal with 
multiple objects that represents only one model and it dimensions properties, 
this module is for you.

It solves problems with models with multiple objects in it composition woth irregular transforms,
using always real dimensions for all operations. including getting model real dimensions, resizing,
transform, origins and more.

*************
Documentation
*************

To build the documentation, run the following command from the root of the

repository::

    python -m pip install sphinx
    sphinx-build -b html docs/source/ docs/build/html

The documentation will be built under ``docs/build/html``. after that, open the index.html file.
in any browser.


