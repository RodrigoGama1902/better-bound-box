import bpy # type:ignore  

from .src.better_bound_box.utils import (
    init_bound_box,
    center_objects_by_center,
    center_objects_by_bottom_center,
    scale_objects_to_height,
    scale_objects_to_width,
    scale_objects_to_depth,
    scale_objects_to_max
)

# ------------------------------------------------------------------------
#   One-file add-on to test the Better Object Bound Box
# ------------------------------------------------------------------------

bl_info = {
    "name": "Better Bound Box",
    "author": "Rodrigo Gama",
    "version": (0, 0, 1),
    "blender": (3, 5, 0),
    "category": "3D View",
}

class BOBB_PT_TestPanel(bpy.types.Panel):
    bl_label = "Better Object Bound Box Tests"
    bl_idname = "BOBB_PT_TestPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BOBB'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        box = layout.box()

        box.operator("bobb.test_operator", text = "init_bound_box").test_operaration = "init_bound_box"
        box.operator("bobb.test_operator", text = "center_objects_by_center").test_operaration = "center_objects_by_center"
        box.operator("bobb.test_operator", text = "center_object_by_bottom_center").test_operaration = "center_object_by_bottom_center"
        box.operator("bobb.test_operator", text = "scale_object_to_height").test_operaration = "scale_object_to_height"
        box.operator("bobb.test_operator", text = "scale_object_to_width").test_operaration = "scale_object_to_width"
        box.operator("bobb.test_operator", text = "scale_object_to_depth").test_operaration = "scale_object_to_depth"
        box.operator("bobb.test_operator", text = "scale_object_to_max").test_operaration = "scale_object_to_max"

class BOBB_PT_TestOperator(bpy.types.Operator):
    bl_idname = "bobb.test_operator"
    bl_label = "My Operator"

    test_operaration: bpy.props.EnumProperty(
        name = "Test Operation",
        description = "Test Operation",
        items = [
            ("init_bound_box", "", ""),
            ("center_objects_by_center", "", ""),
            ("center_object_by_bottom_center", "", ""),
            ("scale_object_to_height", "", ""),
            ("scale_object_to_width", "", ""),
            ("scale_object_to_depth", "", ""),
            ("scale_object_to_max", "", "")
        ]
    ) # type:ignore

    def init_bound_box(self, context):
        objs = bpy.context.selected_objects
        init_bound_box(context, objs, debug = True)

    def center_objects_by_center(self, context):
        objs = bpy.context.selected_objects
        center_objects_by_center(context, objs, debug = True)

    def center_objects_by_bottom_center(self, context):
        objs = bpy.context.selected_objects
        center_objects_by_bottom_center(context, objs, debug = True)

    def scale_object_to_height(self, context):
        objs = bpy.context.selected_objects
        scale_objects_to_height(context, objs, 2, debug = True)

    def scale_object_to_width(self, context):
        objs = bpy.context.selected_objects
        scale_objects_to_width(context, objs, 2, debug = True)

    def scale_object_to_depth(self, context):
        objs = bpy.context.selected_objects
        scale_objects_to_depth(context, objs, 2, debug = True)

    def scale_object_to_max(self, context):
        objs = bpy.context.selected_objects
        scale_objects_to_max(context, objs, 1, 1, 1, debug = True)

    def execute(self, context):
        match self.test_operaration:
            case "init_bound_box":
                self.init_bound_box(context)
            case "center_objects_by_center":
                self.center_objects_by_center(context)
            case "center_object_by_bottom_center":
                self.center_objects_by_bottom_center(context)
            case "scale_object_to_height":
                self.scale_object_to_height(context)
            case "scale_object_to_width":
                self.scale_object_to_width(context)
            case "scale_object_to_depth":
                self.scale_object_to_depth(context)
            case "scale_object_to_max":
                self.scale_object_to_max(context)
            
        return {'FINISHED'}

def register():

    bpy.utils.register_class(BOBB_PT_TestPanel)
    bpy.utils.register_class(BOBB_PT_TestOperator)

def unregister():

    bpy.utils.unregister_class(BOBB_PT_TestPanel)
    bpy.utils.unregister_class(BOBB_PT_TestOperator)

if __name__ == "__main__":
    register()