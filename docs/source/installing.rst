.. _installation:

Installation
------------

To use this submodule in your Blender Add-on, all you have to do is to copy the ``better_bound_box`` folder into your add-on folder 
and import it in your add-on ``__init__.py`` file and add it to the ``sys.path``.

.. tip:: For better organization, you can create a ``libs`` folder in your add-on folder and copy
    the ``better_bound_box`` folder inside it.
    
    This is how the folder structure should look like:

    .. code-block:: bash

        source # This is your add-on development/source folder
        ├── addon 
        ├── libs
        │   └── better-bound-box # This is the better-bound-box submodule repository
        │       └── src
        └── __init__.py # This is your add-on __init__.py file

Here is an code example of how to use the module in your add-on:

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