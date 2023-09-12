'''Utils module for the better_object_bound_box addon

This module provides a set of functions to use the bound box funtionality
but without interacting with the BoundBox class directly. It's a more user
friendly way to use the addon.
'''

from .bound_box import BoundBox

def center_objects_by_center(context, objs) -> None:
    '''Center objects by center of the bound box in the scene'''

    bound_box = BoundBox(context, objs)

    bound_box.set_origin(context, location = bound_box.get_center())
    bound_box.set_location(location = (0,0,0))

def center_objects_by_bottom_center(context, objs) -> None:
    '''Center objects by bottom center of the bound box in the scene'''

    bound_box = BoundBox(context, objs)

    bound_box.set_origin(context, location = bound_box.get_bottom_center())
    bound_box.set_location(location = (0,0,0))

def scale_objects_to_height(context, objs, height) -> None:
    '''Scale objects to the given height'''
    
    bound_box = BoundBox(context, objs)
    bound_box.scale_to_height(height)

def scale_objects_to_width(context, objs, width) -> None:
    '''Scale objects to the given width'''

    bound_box = BoundBox(context, objs)  
    bound_box.scale_to_width(width)

def scale_objects_to_depth(context, objs, depth) -> None:
    '''Scale objects to the given depth'''

    bound_box = BoundBox(context, objs) 
    bound_box.scale_to_depth(depth)

def scale_objects_to_max(context, objs, max_with =1, max_height = 1, max_depth = 1) -> None:
    '''Scale objects to the given max dimension. It takes the highest 
    dimension of the bound box and scales this dimension to it max value.
    
    Ex: if this function is used in a object that has a bound box of width=2, height=3 and depth=4, 
    and the max values passed to the functions are 3, 3 and 3 respectively, the object will be scaled based on the depth dimension,
    because it's the highest dimension of the bound box'''

    bound_box = BoundBox(context, objs)
    
    if (bound_box.get_real_width() >= bound_box.get_real_height()) and (bound_box.get_real_width() >= bound_box.get_real_depth()):
        bound_box.scale_to_width(max_with)
        return 
    if (bound_box.get_real_height() >= bound_box.get_real_width()) and (bound_box.get_real_height() >= bound_box.get_real_depth()):
        bound_box.scale_to_height(max_height)
        return 
    if (bound_box.get_real_depth() >= bound_box.get_real_width()) and (bound_box.get_real_depth() >= bound_box.get_real_height()):
        bound_box.scale_to_depth(max_depth)
        return

  
    
    


