Usage
=====

There is two ways of using this Blender submodule, you can directly use the :class:`~better_bound_box.bound_box.BoundBox`
class, or just use all utility functions from :mod:`~better_bound_box.utils`, the differences will be explained
later in this page.

BoundBox method
---------------

When using the :class:`~better_bound_box.bound_box.BoundBox` class directly, you will have to create a BoundBox 
instance passing your models objects as parameter, and then all the needed methods will be available. it's useful because you will have access to all 
basic operations of the BoundBox class. and from then, you can use all methods as needed.

You can access all the BoundBox methods in the :class:`~better_bound_box.bound_box.BoundBox` class documentation.

.. code-block:: python

    from better_bound_box import BoundBox

    context = bpy.context # Get the current context
    my_model_objs = bpy.context.selected_objects # Get the objects of your model (in this case, the selected objects)

    bound_box = BoundBox(context, my_model_objs) # Create the BoundBox instance
    model_bottom_center = bound_box.get_bottom_center() # Get the bottom center of the model

When using the BoundBox class, you can enable the debug mode, so you can see the bounding box representation
of your model. To enable the debug mode, just call the :meth:`~better_bound_box.bound_box.BoundBox.debug` in 
the BoundBox instance.

.. code-block:: python
    
    bound_box.debug(context) # Enable the debug mode

Utils module method
-------------------

Using the :mod:`~better_bound_box.utils` module, is lot easier because you don't have to create 
an BoundBox instance, just pass the list of objects of your model to the functions and it will automatically 
handle it for you. it's useful if you want to use an specific function that already does exaclty what you need.

You can access all the utils module functions in the :mod:`~better_bound_box.utils` module documentation.

bringing back the code example from this document introduction, if you want to center multiple objects in
the scene world origin, there is two ways of doing it:

.. code-block:: python

    # Using the BoundBox class directly

    from better_bound_box import BoundBox

    my_model_objs = bpy.context.selected_objects

    bound_box = BoundBox(context, my_model_objs) # Create the BoundBox instance
    model_bottom_center = bound_box.get_bottom_center() # Get the bottom center of the model
    bound_box.set_origin(context, location = model_bottom_center) # Set the model origin to the bottom center
    bound_box.set_location(location = (0,0,0)) # Set the model location to the scene world origin

.. code-block:: python

    # Using the utils module

    from better_bound_box.utils import center_objects_by_bottom_center

    my_model_objs = bpy.context.selected_objects
    center_objects_by_bottom_center(context, my_model_objs) # Center the model in the scene world origin

Conclusion
----------

As you can see in the example above, the :mod:`~better_bound_box.utils` module is lot easier to use because it
already does all the work for you, and you don't have to create an BoundBox instance. 

But there will be cases where you want some specific behavior, and in this case, you will have to use the
:class:`~better_bound_box.bound_box.BoundBox` class directly.











