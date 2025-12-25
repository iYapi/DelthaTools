import bpy


# ------------------------------------------------------------------------
# ExConfig UI
# ------------------------------------------------------------------------
class ExConfig_PT_Panel(bpy.types.Panel):
    bl_label = "ExConfig"
    bl_idname = "EXCONFIG_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ExToolbox'
    bl_description = "ExConfig panel for MasterX Tools"

    def draw(self, context):
        layout = self.layout
        s = context.scene

        box = layout.box()
        col = box.column(align=True)
        col.label(text="ExConfig Settings.", icon='PREFERENCES')


def register():
    bpy.utils.register_class(ExConfig_PT_Panel)


def unregister():
    bpy.utils.unregister_class(ExConfig_PT_Panel)
