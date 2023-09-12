.. _introduction:

************
Introduction
************

This submodule provides a better BoundBox system for Blender integrations, 
with support for multiple objects at the same time, non destructive transforms operations
and various utility functions to work with.

If you are creating a Blender integration that will deal with 
multiple objects that represents only one model and you need to work with 
its dimensions properties, this module is for you.

It solves all problems related to the default Blender BoundBox system, including problems with
difficulty to get real dimensions data, irregular transforms, problems when dealing with multiple objects.
at the same time. All of this keeping intact the original objects transforms from the model.

Code examples:

.. code-block:: python

    # Returns the center point from all selected objects at once

    from better_bound_box import BoundBox

    my_model_objs = bpy.context.selected_objects
    bound_box = BoundBox(context, my_model_objs)

    center_point = bound_box.get_center()
    print(center_point)

.. code-block:: python

    # Get bottom center point all selected models, all origins and move it to the world origin.
    # (It is very useful to set the origin of the model that has multiple objects in its composition)
    
    from better_bound_box import BoundBox

    my_model_objs = bpy.context.selected_objects

    bound_box = BoundBox(context, my_model_objs)

    model_bottom_center = bound_box.get_bottom_center()
    bound_box.set_origin(context, location = model_bottom_center)
    bound_box.set_location(location = (0,0,0))

    # Note: There is an specific utility funtion for this operation,
    # but it is just an example of how to use the BoundBox class.

.. code-block:: python

    # Takes an model with multiple objects in it composition and
    # scales it to a fixed width, keeping the proportions for all objects.

    from better_bound_box.utils import scale_objects_to_width

    my_model_objs = bpy.context.selected_objects
    scale_objects_to_width(my_box_objs, 2.0)

.. tip:: This library has a working test add-on that can be used to test some of this library features.
    you can find it in the :ref:`test_addon` section.





