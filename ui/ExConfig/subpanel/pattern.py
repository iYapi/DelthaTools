import bpy


# ------------------------------------------------------------------------
# ExConfig Pattern
# ------------------------------------------------------------------------
class ExConfigPatternUI(bpy.types.Panel):
    bl_label = "ExConfig Pattern"
    bl_idname = "EXCONFIG_PATTERN_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ExToolbox'
    bl_description = "Pattern ExConfig settings for MasterX Tools"
    bl_parent_id = "EXCONFIG_PT_panel"
    bl_order = 2

    def draw(self, context):
        layout = self.layout
        s = context.scene

        box = layout.box()
        col = box.column(align=True)
        col.label(text="Pattern ExConfig.", icon='PREFERENCES')
        col.prop(s.exconfig, "project_pattern_division", text="Division")
        col.prop(s.exconfig, "project_pattern_name", text="Name")
        col.prop(s.exconfig, "project_pattern_base", text="Base")
        col.prop(s.exconfig, "project_pattern_example", text="Example")


def register():
    bpy.utils.register_class(ExConfigPatternUI)


def unregister():
    bpy.utils.unregister_class(ExConfigPatternUI)
