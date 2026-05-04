import bpy


# ------------------------------------------------------------------------
# ExLauncher UI
# ------------------------------------------------------------------------
class EXLAUNCHER_PT_Panel(bpy.types.Panel):
    bl_label = "DelthλLauncher"
    bl_idname = "EXLAUNCHER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'DelthλTools'
    bl_description = "ExLauncher panel for MasterX Tools"

    def draw(self, context):
        layout = self.layout
        s = context.scene
        exlauncher = s.exlauncher

        box = layout.box()
        col = box.column(align=True)
        col.label(text="DelthλLauncher Settings", icon='MEMORY')

        col.prop(exlauncher, "version_type", text="Version Type")

        col.separator()

        row = col.row(align=True)
        row.operator("exlauncher.save_progress", text="Save Progress", icon='FILE_BACKUP')
        row.operator("exlauncher.save_master", text="Save Master", icon='FILE_BLEND')


def register():
    bpy.utils.register_class(EXLAUNCHER_PT_Panel)


def unregister():
    bpy.utils.unregister_class(EXLAUNCHER_PT_Panel)
