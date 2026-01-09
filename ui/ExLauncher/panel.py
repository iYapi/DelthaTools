import bpy


# ------------------------------------------------------------------------
# ExLauncher UI
# ------------------------------------------------------------------------
class EXLAUNCHER_PT_Panel(bpy.types.Panel):
    bl_label = "ExLauncher"
    bl_idname = "EXLAUNCHER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ExToolbox'
    bl_description = "ExLauncher panel for MasterX Tools"

    def draw(self, context):
        layout = self.layout
        s = context.scene
        exlauncher = s.exlauncher

        box = layout.box()
        col = box.column(align=True)
        col.label(text="ExLauncher Settings", icon='ROCKET')

        col.prop(exlauncher, "version_type", text="Version Type")

        col.separator()
        col.operator("exlauncher.save_progress", text="Save Progress", icon='FILE_TICK')
        col.operator("exlauncher.save_master", text="Save Master", icon='SAVE_AS')


def register():
    bpy.utils.register_class(EXLAUNCHER_PT_Panel)


def unregister():
    bpy.utils.unregister_class(EXLAUNCHER_PT_Panel)
