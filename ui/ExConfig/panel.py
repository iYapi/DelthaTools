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
        
        # Header row with title and refresh button
        row = col.row(align=True)
        row.label(text="ExConfig Settings.", icon='PREFERENCES')
        row.operator("exconfig.refresh_data", text="", icon='FILE_REFRESH')
        
        col.prop(s.exconfig, "project_list", text="Project")
        
        # Show pattern selector if a project is selected
        if s.exconfig.project_list != 'NONE':
            col.prop(s.exconfig, "project_pattern_selected", text="Pattern")
        
        # Split row for load buttons
        row = col.row(align=True)
        row.operator("exconfig.load_selected_project", text="Load Project", icon='IMPORT')
        row.operator("exconfig.load_config_file", text="Browse", icon='FILE_FOLDER')
        
        col.separator()
        col.operator("exconfig.generate_config", text="Save Settings", icon='FILE_TICK')


def register():
    bpy.utils.register_class(ExConfig_PT_Panel)


def unregister():
    bpy.utils.unregister_class(ExConfig_PT_Panel)
