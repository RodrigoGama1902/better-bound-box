import bpy #type:ignore
import bmesh #type:ignore

def add_display_point(context, name, location, size = 0.1, mesh_type = "CUBE"):
    '''Add a display point to the scene. A display point is a cube that is used
    to debug the bound box calculations. It is not used in the final result. 

    *name* - name of the display point object, it will be used to check if 
    the object already exists, if it does it will be removed and replaced with

    *location* - location of the display point

    *size* - size of the display point

    *type* - type of the display point, it can be "CUBE", "SPHERE" or "CIRCLE"

    '''

    if bpy.data.objects.get(name):
        bpy.data.objects.remove(bpy.data.objects.get(name), do_unlink=True)

    match mesh_type:
        case "CUBE":
            bpy.ops.mesh.primitive_cube_add(size = size, location = location)
        case "SPHERE":
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius = size, 
                location = location,
                segments = 8,
                ring_count = 5
            )

        case "CIRCLE":
            bpy.ops.mesh.primitive_circle_add(radius = size, location = location)

    obj = context.active_object
    obj.name = name
    obj.display_type = 'WIRE'
    obj.show_in_front = True
    obj.show_name = True
    obj.hide_select = True

def add_bound_box_viewport(
        context, 
        name,
        width,
        height, 
        depth,
        center_position):
    '''Add a bound box to the scene. A bound box is a cube that is used'''

    if bpy.data.objects.get(name):
        bpy.data.objects.remove(bpy.data.objects.get(name), do_unlink=True)

    mesh = bpy.data.meshes.new(name="CubeMesh")
    obj = bpy.data.objects.new(name, mesh)

    # Link the object to the scene
    bpy.context.scene.collection.objects.link(obj)

    # Select the new object
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Create a bmesh cube and scale it
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, height, depth))

    # Update the mesh with the bmesh data
    bm.to_mesh(mesh)
    bm.free()

    # Set the location of the cube
    obj.location = center_position

    # Update the cube's dimensions in the object data
    obj.dimensions = (width, depth, height)
    obj = context.active_object
    obj.display_type = 'WIRE'
    obj.show_in_front = True
    obj.show_name = True
    obj.hide_select = True
    
