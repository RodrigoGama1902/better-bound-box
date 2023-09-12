
import bpy #type:ignore
import bmesh #type:ignore

import statistics
from .debug_utils import add_display_point

class BoundBox:

    def __init__(self, context, objs : list[bpy.types.Object], apply_transform : bool = True):
        ''' BoundBox initialization class

        :param context: context of the operator
        :type context: bpy.context
        :param objs: objects to calculate the bound box
        :type objs: list[bpy.types.Object]
        :param apply_transform: apply transform to the objects before calculating the bound box, 
            it's optional, but it's recommended to apply the transform before calculating the bound box
        :type apply_transform: bool

        '''

        self.objs = objs

        if apply_transform:
            self._apply_transform(context)

        self.bv = BoundVectors(objs)

    def _apply_transform(self, context) -> None:
        '''Apply transform to the objects. this method is context destructive
        so it automatically fix the selection and active object after applying the transform'''
        
        # Storing original values
        original_selected_objs = context.selected_objects.copy()
        original_active_obj = context.view_layer.objects.active

        # Fixing selection
        bpy.ops.object.select_all(action='DESELECT')
        for ob in self.objs:
            ob.select_set(True)
            context.view_layer.objects.active = ob

        # Executing
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        # Restoring original values
        for ob in original_selected_objs:
            ob.select_set(True)
        context.view_layer.objects.active = original_active_obj

    def get_center(self) -> tuple[float, float, float]:
        '''Get center of the object'''

        return ((self.bv.max_vertex_x[0] + self.bv.min_vertex_x[0])/2,
                (self.bv.max_vertex_y[1] + self.bv.min_vertex_y[1])/2,
                (self.bv.max_vertex_z[2] + self.bv.min_vertex_z[2])/2)
    
    def get_bottom_center(self) -> tuple[float, float, float]:
        '''Get bottom center of the object'''

        return ((self.bv.max_vertex_x[0] + self.bv.min_vertex_x[0])/2,
                (self.bv.max_vertex_y[1] + self.bv.min_vertex_y[1])/2,
                self.bv.min_vertex_z[2])
    
    def get_hight_vectors(self) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        '''Get height min and max vector points'''

        v1 = [self.bv.min_vertex_x[0], self.bv.min_vertex_y[1], self.bv.min_vertex_z[2]]
        v2 = [self.bv.min_vertex_x[0], self.bv.min_vertex_y[1], self.bv.max_vertex_z[2]]
        
        return v1, v2

    def get_width_vectors(self) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        '''Get width min and max vector points'''

        v1 = [self.bv.min_vertex_x[0], self.bv.min_vertex_y[1], self.bv.min_vertex_z[2]]
        v2 = [self.bv.max_vertex_x[0], self.bv.min_vertex_y[1], self.bv.min_vertex_z[2]]
        
        return v1, v2
        
    def get_depth_vectors(self) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        '''Get depth min and max vector points'''

        v1 = [self.bv.max_vertex_x[0], self.bv.min_vertex_y[1], self.bv.min_vertex_z[2]]
        v2 = [self.bv.max_vertex_x[0], self.bv.max_vertex_y[1], self.bv.min_vertex_z[2]]
        
        return v1, v2

    def get_real_height(self, round_value : int = 2) -> float:
        '''Get real height of the bound box'''

        return round(self.bv.max_vertex_z[2] - self.bv.min_vertex_z[2], round_value)

    def get_real_width(self, round_value : int = 2) -> float:
        '''Get real width of the bound box'''

        return round(self.bv.max_vertex_x[0] - self.bv.min_vertex_x[0], round_value)
    
    def get_real_depth(self, round_value : int = 2) -> float:
        '''Get real depth of the bound box'''

        return round(self.bv.max_vertex_x[0] - self.bv.max_vertex_y[1], round_value)
   
    def get_largest_dimension(self) -> float:
        '''Get largest dimension of the bound box (height, width or depth)'''

        return max(
            self.get_real_height(), 
            self.get_real_width(),
            self.get_real_depth()
            )
 
    def get_mean_dimension(self) -> float:
        '''Get mean dimension of the object'''

        return statistics.mean([
            self.get_real_height(),
            self.get_real_width(), 
            self.get_real_depth()]
        )
    
    def debug(self, context) -> None:
        '''Enable debug mode, when enabled it will display each 
        bound box vector in the viewport as a point'''

        self.bv.debug(context)

        add_display_point(context, "center", self.get_center(), viewport_color = (0,1,0,1), size = 0.2)
        add_display_point(context, "bottom_center", self.get_bottom_center(), viewport_color = (0,1,0,1), size = 0.2)

    def set_origin(self, context, location : tuple[int, int, int] = (0,0,0)) -> None:
        '''Set origin of the object to the given location, this method is context destructive
        so it automatically fix the selection and active object after applying the transform'''

        # Storing original values
        original_selected_objs = context.selected_objects.copy()
        original_active_obj = context.view_layer.objects.active
        original_cursor_location = context.scene.cursor.location.copy()

        # Fixing selection
        bpy.ops.object.select_all(action='DESELECT')
        for ob in self.objs:
            ob.select_set(True)
            context.view_layer.objects.active = ob

        # Executing
        context.scene.cursor.location = location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR') 

        # Restoring original values
        for ob in original_selected_objs:
            ob.select_set(True)

        context.view_layer.objects.active = original_active_obj
        context.scene.cursor.location = original_cursor_location

    def set_location(self, location : tuple[int, int, int] = (0,0,0)) -> None:
        '''Set location of the object to the given location'''

        for ob in self.objs:
            ob.location = location

    def scale_to_height(self, height) -> None:
        '''Scale object to the given height'''

        scale = height / self.get_real_height()

        for ob in self.objs:
            ob.scale = (scale, scale, scale)

    def scale_to_width(self, width) -> None:
        '''Scale object to the given width'''

        scale = width / self.get_real_width()

        for ob in self.objs:
            ob.scale = (scale, scale, scale)

    def scale_to_depth(self, depth) -> None:
        '''Scale object to the given depth'''

        scale = depth / self.get_real_depth()

        for ob in self.objs:
            ob.scale = (scale, scale, scale)

class BoundVectors:
    '''Generates all vector min and max values of the objs'''
    
    max_vertex_x : list[float] 
    max_vertex_y : list[float] 
    max_vertex_z : list[float]
            
    min_vertex_x : list[float]
    min_vertex_y : list[float] 
    min_vertex_z : list[float] 
    
    def __init__(self, objs): 
        
        self.max_vertex_x = []
        self.max_vertex_y = []
        self.max_vertex_z = []
                
        self.min_vertex_x = []
        self.min_vertex_y = []
        self.min_vertex_z = []
        
        self._get_objs_bound_vectors(objs)
                
    @staticmethod
    def _get_object_vertices(objs):
        '''Get all vertices of the objects'''

        total_verts = []

        bpy.ops.object.select_all(action='DESELECT')
        
        for ob in objs: 
                    
            if not ob.type == "MESH":
                continue
            
            ob.select_set(True)   
            bpy.context.view_layer.objects.active = ob     
            bpy.ops.object.mode_set(mode='EDIT')
            
            me = ob.data    
            bm = bmesh.from_edit_mesh(me)
            
            total_verts.extend([[v.co[0],
                                    v.co[1],
                                    v.co[2]] for v in bm.verts])

            bpy.ops.object.mode_set(mode='OBJECT')
        
        return total_verts

    def _get_objs_bound_vectors(self, objs):
        '''Get all bound vectors of the objects'''
                
        total_verts = self._get_object_vertices(objs)
                
        for v in total_verts:
            
            if not self.max_vertex_x:
                self.max_vertex_x = v
            if not self.max_vertex_y:
                self.max_vertex_y = v
            if not self.max_vertex_z:
                self.max_vertex_z = v
                
            if not self.min_vertex_x:
                self.min_vertex_x = v
            if not self.min_vertex_y:
                self.min_vertex_y = v
            if not self.min_vertex_z:
                self.min_vertex_z = v
            
            if v[0] >= self.max_vertex_x[0]:
                self.max_vertex_x = v
            if v[1] >= self.max_vertex_y[1]:
                self.max_vertex_y = v             
            if v[2] >= self.max_vertex_z[2]:
                self.max_vertex_z = v  
                            
            if v[0] <= self.min_vertex_x[0]:
                self.min_vertex_x = v              
            if v[1] <= self.min_vertex_y[1]:
                self.min_vertex_y = v           
            if v[2] <= self.min_vertex_z[2]:
                self.min_vertex_z = v
                
        bpy.ops.object.mode_set(mode='OBJECT')  

    def debug(self, context):
        '''Enable debug mode, when enabled it will display each 
        bound box vector in the viewport as a point'''

        add_display_point(context, "max_x", self.max_vertex_x)
        add_display_point(context, "max_y", self.max_vertex_y)
        add_display_point(context, "max_z", self.max_vertex_z)

        add_display_point(context, "min_x", self.min_vertex_x)
        add_display_point(context, "min_y", self.min_vertex_y)
        add_display_point(context, "min_z", self.min_vertex_z)


        
       



        
