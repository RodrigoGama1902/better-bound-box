
import bpy #type:ignore
import bmesh #type:ignore
import mathutils #type:ignore

import statistics

from .debug_utils import (
    add_display_point, 
    add_bound_box_viewport)

class BoundVectors:
    '''Generates all vector min and max values of the objs'''
    
    max_vertex_x : list[float] 
    max_vertex_y : list[float] 
    max_vertex_z : list[float]
            
    min_vertex_x : list[float]
    min_vertex_y : list[float] 
    min_vertex_z : list[float] 
    
    def __init__(self, objs): 
        
        self.objs = objs    
        self._get_objs_bound_vectors(objs)
    
    @staticmethod
    def _get_object_vertices(objs) -> dict[bpy.types.Object, list[list[float]]]:
        '''Get all vertices of the objects'''

        total_verts = {}

        for ob in objs:
            if not ob.type == "MESH":
                continue

            me = ob.data
            bm = bmesh.new()
            bm.from_mesh(me)

            total_verts[ob] = [[v.co[0], v.co[1], v.co[2]] for v in bm.verts]

            bm.free()

        return total_verts

    def _get_objs_bound_vectors(self, objs):
        '''Get all bound vectors of the objects'''
                
        self.max_vertex_x = []
        self.max_vertex_y = []
        self.max_vertex_z = []
                
        self.min_vertex_x = []
        self.min_vertex_y = []
        self.min_vertex_z = []

        vertex_data: dict[bpy.types.Object, list[list[float]]] = self._get_object_vertices(objs)
    
        for ob in vertex_data:
            # Get the object's transformation matrix
            obj_matrix = ob.matrix_world
            
            for v in vertex_data[ob]:
                # Apply the object's transformation to the vertex
                transformed_vertex = obj_matrix @ mathutils.Vector(v)
                
                if not self.max_vertex_x:
                    self.max_vertex_x = transformed_vertex
                if not self.max_vertex_y:
                    self.max_vertex_y = transformed_vertex
                if not self.max_vertex_z:
                    self.max_vertex_z = transformed_vertex
                    
                if not self.min_vertex_x:
                    self.min_vertex_x = transformed_vertex
                if not self.min_vertex_y:
                    self.min_vertex_y = transformed_vertex
                if not self.min_vertex_z:
                    self.min_vertex_z = transformed_vertex
                
                if transformed_vertex[0] >= self.max_vertex_x[0]:
                    self.max_vertex_x = transformed_vertex
                if transformed_vertex[1] >= self.max_vertex_y[1]:
                    self.max_vertex_y = transformed_vertex             
                if transformed_vertex[2] >= self.max_vertex_z[2]:
                    self.max_vertex_z = transformed_vertex  
                                
                if transformed_vertex[0] <= self.min_vertex_x[0]:
                    self.min_vertex_x = transformed_vertex              
                if transformed_vertex[1] <= self.min_vertex_y[1]:
                    self.min_vertex_y = transformed_vertex           
                if transformed_vertex[2] <= self.min_vertex_z[2]:
                    self.min_vertex_z = transformed_vertex
        

    def debug(self, context):
        '''Enable debug mode, when enabled it will display each 
        bound box vector in the viewport as a point'''

        add_display_point(context, "max_x", self.max_vertex_x)
        add_display_point(context, "max_y", self.max_vertex_y)
        add_display_point(context, "max_z", self.max_vertex_z)

        add_display_point(context, "min_x", self.min_vertex_x)
        add_display_point(context, "min_y", self.min_vertex_y)
        add_display_point(context, "min_z", self.min_vertex_z)

    def update(self):
        '''Update bound vectors of the objects'''
        self._get_objs_bound_vectors(self.objs)



class BoundBox:

    objs : list[bpy.types.Object]
    bv : BoundVectors

    def __init__(
            self, 
            context, 
            objs : list[bpy.types.Object], 
            ):
        ''' BoundBox initialization class

        :param context: context of the operator
        :type context: bpy.context
        :param objs: objects to calculate the bound box
        :type objs: list[bpy.types.Object]

        '''

        self.objs = objs
        self.bv = BoundVectors(objs)

    @staticmethod
    def _object_selection_context(func):
        '''Decorator to select objects before executing a method
        and deselect them after the execution of the method
        
        It should be used for methods that needs selected objects to work        
        '''

        def wrapper(self, context, *args, **kwargs):
            # Deselecting all objects
            bpy.ops.object.select_all(action='DESELECT')
            
            # Selecting
            for ob in self.objs:
                ob.select_set(True)
            context.view_layer.objects.active = self.objs[0]
        
            func(self, context, *args, **kwargs)
            
            # Deselecting
            for ob in self.objs:
                ob.select_set(False)

        return wrapper


    def _update_vectors(self, context) -> None:
        '''Update bound vectors of the objects
        
        This method is called after the execution of any method that changes 
        the current bound box of the object
        
        '''
        context.view_layer.update()
        self.bv.update()


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
    

    def get_hight_vectors(self) -> tuple[list[float], list[float]]:
        '''Get height min and max vector points'''

        v1 = [self.bv.min_vertex_x[0], self.bv.min_vertex_y[1], self.bv.min_vertex_z[2]]
        v2 = [self.bv.min_vertex_x[0], self.bv.min_vertex_y[1], self.bv.max_vertex_z[2]]
        
        return v1, v2


    def get_width_vectors(self) -> tuple[list[float], list[float]]:
        '''Get width min and max vector points'''

        v1 = [self.bv.min_vertex_x[0], self.bv.min_vertex_y[1], self.bv.min_vertex_z[2]]
        v2 = [self.bv.max_vertex_x[0], self.bv.min_vertex_y[1], self.bv.min_vertex_z[2]]
        
        return v1, v2
        

    def get_depth_vectors(self) -> tuple[list[float], list[float]]:
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

        return round(self.bv.max_vertex_y[1] - self.bv.min_vertex_y[1], round_value)
   

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
    
    @_object_selection_context
    def set_origin(self, context, location : tuple[float, float, float] = (0,0,0)) -> None:
        '''Set origin of the object to the given location, this method is context destructive
        so it automatically fix the selection and active object after applying the transform'''

        # Executing
        context.scene.cursor.location = location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR') 

        self._update_vectors(context)

    @_object_selection_context
    def _scale_to_factor(self, context, value, factor):
        ''' Scale object to the given factor dimension factor, 
        ex: if the factor is 2, the object will be scaled to 2 times it's original size'''

        scale = value / factor
        bpy.ops.transform.resize(value=(scale, scale, scale), orient_type='LOCAL') 

        self._update_vectors(context)


    def set_location(self, context, location : tuple[int, int, int] = (0,0,0)) -> None:
        '''Set location of the object to the given location and '''

        for ob in self.objs:
            ob.location = location
        self._update_vectors(context)


    def scale_to_height(self, context, height) -> None:
        '''Scale object to the given height and apply the transform'''

        self._scale_to_factor(context, height, self.get_real_height())


    def scale_to_width(self, context, width) -> None:
        '''Scale object to the given width and apply the transform'''

        self._scale_to_factor(context, width, self.get_real_width())


    def scale_to_depth(self, context, depth) -> None:
        '''Scale object to the given depth and apply the transform'''

        self._scale_to_factor(context, depth, self.get_real_depth())
    

    def debug(self, context) -> None:
        '''Enable debug mode, when enabled it will display each 
        bound box vector in the viewport as a point'''

        self.bv.debug(context)

        add_display_point(context, "center", self.get_center(), size = 0.05, mesh_type="SPHERE")
        add_display_point(context, "bottom_center", self.get_bottom_center(), size = 0.2, mesh_type="CIRCLE")

        add_bound_box_viewport(
            context, 
            "bound_box",
            self.get_real_width(),
            self.get_real_height(),
            self.get_real_depth(),
            self.get_center()
        )
 

