.. _test_addon:

Test Addon
------------

You can use this submodule repository as a Blender add-on installation, 
so you can test the functionality of it. To install it just zip the submodule repository folder 
and install it as a Blender add-on. The add-on can be found in the ``3D View`` in a tab named ``BOBB``.

Here are the current test operators shown in the add-on panel:

.. note::
    The test operators are only available in the ``Object Mode``. to use it, just select multiple objects
    and click on the operator button.

- ``init_bound_box`` - executes :func:`better_bound_box.utils.init_bound_box`
- ``center_objects_by_center`` - executes :func:`better_bound_box.utils.center_objects_by_center`
- ``center_object_by_bottom_center`` - executes :func:`better_bound_box.utils.center_object_by_bottom_center`
- ``scale_object_to_height`` - executes :func:`better_bound_box.utils.scale_object_to_height` with the value of ``2.0``
- ``scale_object_to_width`` - executes :func:`better_bound_box.utils.scale_object_to_width` with the value of ``2.0``
- ``scale_object_to_depth`` - executes :func:`better_bound_box.utils.scale_object_to_depth` with the value of ``2.0``
- ``scale_object_to_max`` - executes :func:`better_bound_box.utils.scale_object_to_max` with the value of ``(1,1,1)``



