import glob
import bpy
import bmesh
from mathutils import Vector, Matrix



def create_hull():
    # CONVERTS TO CONVEX HULL
    context = bpy.context
    scene = context.scene
    ob = context.object
    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)
    copy = ob.copy()
    ch = bpy.data.meshes.new("%s convexhull" % me.name)
    bmesh.ops.convex_hull(bm, input=bm.verts)
    bm.to_mesh(ch)
    copy.name = "%s (hull)" % ob.name
    copy.data = ch
    scene.objects.link(copy)
    # bpy.ops.outliner.object_operation(TYPE="DESELECT")
    return copy, ob
    
def remesh(obj, original):
    ''' remeshes a convex hull with smoothing settings to around 8 octotree '''
    bpy.context.scene.objects.active = obj

    # TODO: separate into separate function
    remesher = obj.modifiers.new(name="Remesh", type="REMESH")
    remesher.octree_depth = 6
    remesher.mode = "SMOOTH"
    remesher.use_smooth_shade = True
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Remesh")

    # TODO: separate into separate function
    shrinker = obj.modifiers.new(name="Shrinkwrap", type="SHRINKWRAP")
    shrinker.target = bpy.data.objects[original.name]
    shrinker.wrap_method = 
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Shrinkwrap")

    # TODO: separate into separate function
    smoother = obj.modifiers.new(name="Smooth", type="SMOOTH")
    smoother.factor = 0.9
    smoother.iterations = 30
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Smooth")
    return obj

def singular_select(ob):
    ''' deselects all except the matching object '''
    bpy.context.scene.objects.active = obj
    selected_objects = bpy.context.selected_objects
    for ob in selected_objects:
        if ob == obj:
            ob.select = True
        else:
            print('deselecting: %s' % ob.name)
            ob.select = False

def get_object_volume(obj):
    ''' Returns the volume of the object '''
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    return bm.calc_volume()
    
def create_output_file_name(base_dir, object):
    return base_dir + object.name + '_volume_' + str(round(get_object_volume(object), 3))

base_dir = '/home/warrick/Desktop/roonka_features/'
shapefiles = glob.glob(base_dir + '*.shp')
for shp in shapefiles:
    bpy.ops.importgis.shapefile(filepath=shp)
    convex_hull, original = create_hull()
    obj = remesh(convex_hull, original)
    singular_select(obj)
    bpy.ops.export_mesh.stl(filepath=create_output_file_name(base_dir, obj), use_selection=True)
    # TODO: May need to do something regarding multipatches?
    # TODO: adding a workflow which smooths out big extrusions such as in F142. Potentially using Opensubdiv and catmull clark subdivision.