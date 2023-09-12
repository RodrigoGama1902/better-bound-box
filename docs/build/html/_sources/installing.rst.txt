.. _installation:

Installation
------------

To use this module in your Blender Add-on, the easiest way add to your project is to clone the repository into a 
``libs`` folder and add the following code to the top of your add-on ``__init__.py`` file:

This is how the folder structure should look like:

.. code-block:: bash

    source # This is your add-on development/source folder
    ├── addon 
    ├── libs
    │   └── better-bound-box # This is the better-bound-box module repository
    │       └── src
    └── __init__.py # This is your add-on __init__.py file

Here is the code to add to your ``__init__.py`` file:

.. code-block:: python

    bl_info = {
        "name": "My Add-on",
        "description": "My Add-on description",
        "author": "Me",
        "version": (0, 1, 4),
        "blender": (3, 2, 0),
        "location": "View3D",
        "category": "3D View"}

    import os
    import sys

    _cwd = os.path.dirname(__file__)
    sys.path.append(os.path.abspath(os.path.join(_cwd, 'libs', 'better-bound-box', 'src')))

    def register():
        from .addon.register import register_addon
        register_addon()

    def unregister():
        from .addon.register import unregister_addon
        unregister_addon()

After that, you can import the module anywhere in your add-on:

.. code-block:: python

    from better_bound_box import BoundBox