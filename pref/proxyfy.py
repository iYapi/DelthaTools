import bpy
from bpy.props import (
    BoolProperty, FloatProperty, IntProperty, StringProperty,
    EnumProperty, CollectionProperty,
)
from bpy.types import PropertyGroup

# ---------------------------------------------------------------------------
# Property sub-types for list entries
# ---------------------------------------------------------------------------

class ProxyfyNameItem(PropertyGroup):
    name: StringProperty(name="Name")


# ---------------------------------------------------------------------------
# Main settings PropertyGroup
# ---------------------------------------------------------------------------

class ProxyfySettings(PropertyGroup):
    # --- General ---
    apply_mirror_first: BoolProperty(
        name="Apply Mirror First",
        default=True,
    )
    only_groups_with_matching_bone: BoolProperty(
        name="Only Groups Matching Bone",
        default=True,
    )
    make_unassigned_chunk: BoolProperty(
        name="Make UNASSIGNED Chunk",
        default=True,
    )
    unassigned_name: StringProperty(
        name="Unassigned Name",
        default="UNASSIGNED",
    )
    use_child_of_constraint: BoolProperty(
        name="Use Child-Of Constraint",
        default=True,
    )
    use_prefix_srcname: BoolProperty(
        name="Prefix Chunk with Source Name",
        default=True,
    )
    clean_previous_run: BoolProperty(
        name="Clean Previous Run",
        default=True,
    )
    strip_shape_keys: BoolProperty(
        name="Strip Shape Keys (chunks)",
        default=True,
    )
    clean_loose_geometry: BoolProperty(
        name="Clean Loose Geometry",
        default=True,
    )
    decimate_ratio: FloatProperty(
        name="Chunk Decimate Ratio",
        default=1.0, min=0.0, max=1.0,
    )
    join_per_source: BoolProperty(
        name="Join Chunks Per Source",
        default=False,
    )

    # --- Boundary ---
    boundary_mode: EnumProperty(
        name="Boundary Mode",
        items=[
            ('OVERLAP',  "Overlap",  "Face belongs to all bones whose verts influence it"),
            ('MAJORITY', "Majority", "Face belongs to bone with highest total weight"),
            ('SHRINK',   "Shrink",   "Vertex-based strict ownership"),
        ],
        default='OVERLAP',
    )
    weight_threshold: FloatProperty(
        name="Weight Threshold",
        description="Minimum weight to consider a vertex assigned",
        default=0.4, min=0.0, max=1.0,
    )

    # --- Head Mesh ---
    head_mesh_names: CollectionProperty(type=ProxyfyNameItem)
    head_mesh_names_index: IntProperty(default=0)

    head_decimate_type: EnumProperty(
        name="Head Decimate Type",
        items=[
            ('COLLAPSE', "Collapse", "Reduce polygon count"),
            ('UNSUBDIV', "Un-Subdivide", "Undo subdivision"),
            ('DISSOLVE', "Dissolve", "Planar dissolve"),
        ],
        default='COLLAPSE',
    )
    head_decimate_ratio: FloatProperty(
        name="Head Decimate Ratio",
        default=0.13, min=0.0, max=1.0,
    )
    head_decimate_use_symmetry: BoolProperty(
        name="Use Symmetry",
        default=True,
    )
    head_decimate_symmetry_axis: EnumProperty(
        name="Symmetry Axis",
        items=[('X', "X", ""), ('Y', "Y", ""), ('Z', "Z", "")],
        default='X',
    )
    head_decimate_triangulate: BoolProperty(
        name="Triangulate",
        default=True,
    )
    head_apply_subsurf_first: BoolProperty(
        name="Apply Subsurf First",
        default=True,
    )

    # --- Linked Hide ---
    linked_hide_names: CollectionProperty(type=ProxyfyNameItem)
    linked_hide_names_index: IntProperty(default=0)

    # --- Driver ---
    control_bone_name: StringProperty(
        name="Control Bone",
        description="Bone that holds the 'proxy mesh' custom property",
        default="c_pos",
    )
    prop_name: StringProperty(
        name="Property Name",
        default="proxy mesh",
    )
    prop_description: StringProperty(
        name="Property Description",
        default="swap to proxy mesh",
    )
    prop_default_value: IntProperty(
        name="Default Value",
        default=0, min=0, max=1,
    )
    drive_source_visibility: BoolProperty(
        name="Drive Source Visibility",
        default=True,
    )

    # --- Debug ---
    strict_mode: BoolProperty(
        name="Strict Mode",
        description="Abort on first error",
        default=True,
    )
    log_to_file: BoolProperty(
        name="Log to File",
        default=True,
    )

def register():
    bpy.utils.register_class(ProxyfyNameItem)
    bpy.utils.register_class(ProxyfySettings)
    bpy.types.Scene.proxyfy_settings = bpy.props.PointerProperty(type=ProxyfySettings)
    
def unregister():
    bpy.utils.unregister_class(ProxyfyNameItem)
    bpy.utils.unregister_class(ProxyfySettings)
    del bpy.types.Scene.proxyfy_settings