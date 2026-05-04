import os
import tempfile
import bpy
from bpy.types import Panel

# ---------------------------------------------------------------------------
# Panel
# ---------------------------------------------------------------------------

class PROXYFY_PT_main(Panel):
    bl_label = "Proxyfy MK11"
    bl_idname = "PROXYFY_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ExToolbox"

    def draw(self, context):
        layout = self.layout
        s = context.scene.proxyfy_settings

        # Run / Revert
        row = layout.row(align=True)
        row.scale_y = 1.6
        row.operator("proxyfy.run", icon='PLAY')
        row.operator("proxyfy.revert", icon='LOOP_BACK')


# class PROXYFY_PT_general(Panel):
#     bl_label = "General"
#     bl_idname = "PROXYFY_PT_general"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = "Proxyfy"
#     bl_parent_id = "PROXYFY_PT_main"
#     bl_options = {'DEFAULT_CLOSED'}

#     def draw(self, context):
#         layout = self.layout
#         s = context.scene.proxyfy_settings
#         layout.prop(s, "apply_mirror_first")
#         layout.prop(s, "only_groups_with_matching_bone")
#         layout.prop(s, "make_unassigned_chunk")
#         layout.prop(s, "unassigned_name")
#         layout.prop(s, "use_child_of_constraint")
#         layout.prop(s, "use_prefix_srcname")
#         layout.prop(s, "clean_previous_run")
#         layout.prop(s, "strip_shape_keys")
#         layout.prop(s, "clean_loose_geometry")
#         layout.prop(s, "decimate_ratio")
#         layout.prop(s, "join_per_source")


class PROXYFY_PT_boundary(Panel):
    bl_label = "Boundary"
    bl_idname = "PROXYFY_PT_boundary"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ExToolbox"
    bl_parent_id = "PROXYFY_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        s = context.scene.proxyfy_settings
        layout.prop(s, "boundary_mode")
        layout.prop(s, "weight_threshold", slider=True)


class PROXYFY_PT_head(Panel):
    bl_label = "Head Meshes"
    bl_idname = "PROXYFY_PT_head"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ExToolbox"
    bl_parent_id = "PROXYFY_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        s = context.scene.proxyfy_settings

        row = layout.row()
        row.template_list("UI_UL_list", "head_mesh_names",
                          s, "head_mesh_names",
                          s, "head_mesh_names_index",
                          rows=3)
        col = row.column(align=True)
        col.operator("proxyfy.add_head_mesh", icon='ADD', text="")
        col.operator("proxyfy.remove_head_mesh", icon='REMOVE', text="")

        layout.separator()
        layout.prop(s, "head_decimate_type")
        layout.prop(s, "head_decimate_ratio", slider=True)
        # layout.prop(s, "head_decimate_use_symmetry")
        # sub = layout.row()
        # sub.enabled = s.head_decimate_use_symmetry
        # sub.prop(s, "head_decimate_symmetry_axis", expand=True)
        # layout.prop(s, "head_decimate_triangulate")
        # layout.prop(s, "head_apply_subsurf_first")


class PROXYFY_PT_linked_hide(Panel):
    bl_label = "Linked Hide"
    bl_idname = "PROXYFY_PT_linked_hide"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ExToolbox"
    bl_parent_id = "PROXYFY_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        s = context.scene.proxyfy_settings

        row = layout.row()
        row.template_list("UI_UL_list", "linked_hide_names",
                          s, "linked_hide_names",
                          s, "linked_hide_names_index",
                          rows=3)
        col = row.column(align=True)
        col.operator("proxyfy.add_linked_hide", icon='ADD', text="")
        col.operator("proxyfy.remove_linked_hide", icon='REMOVE', text="")


class PROXYFY_PT_driver(Panel):
    bl_label = "Driver / Property"
    bl_idname = "PROXYFY_PT_driver"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ExToolbox"
    bl_parent_id = "PROXYFY_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        s = context.scene.proxyfy_settings
        layout.prop(s, "control_bone_name")
        # layout.prop(s, "prop_name")
        # layout.prop(s, "prop_description")
        # layout.prop(s, "prop_default_value")
        # layout.prop(s, "drive_source_visibility")


class PROXYFY_PT_debug(Panel):
    bl_label = "Debug"
    bl_idname = "PROXYFY_PT_debug"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ExToolbox"
    bl_parent_id = "PROXYFY_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        s = context.scene.proxyfy_settings
        layout.prop(s, "strict_mode")
        layout.prop(s, "log_to_file")
        if s.log_to_file:
            path = os.path.join(tempfile.gettempdir(), "proxyfy_log.txt")
            layout.label(text=path, icon='TEXT')

classes = [
    PROXYFY_PT_main,
    # PROXYFY_PT_general,
    PROXYFY_PT_boundary,
    PROXYFY_PT_head,
    PROXYFY_PT_linked_hide,
    PROXYFY_PT_driver,
    PROXYFY_PT_debug,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)