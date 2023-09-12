import bpy #type:ignore

def add_display_point(context, name, location, size = 0.1):
    '''Add a display point to the scene. A display point is a cube that is used
    to debug the bound box calculations. It is not used in the final result. 

    *name* - name of the display point object, it will be used to check if 
    the object already exists, if it does it will be removed and replaced with

    *location* - location of the display point

    *size* - size of the display point
    '''

    if bpy.data.objects.get(name):
        bpy.data.objects.remove(bpy.data.objects.get(name), do_unlink=True)

    bpy.ops.mesh.primitive_cube_add(size = size, location = location)

    obj = context.active_object
    obj.name = name
    obj.display_type = 'WIRE'
    obj.show_in_front = True
    obj.show_name = True
    obj.hide_select = True
