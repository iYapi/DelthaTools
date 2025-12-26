import bpy


# ------------------------------------------------------------------------
# ExConfig Pattern Match Subpanel
# ------------------------------------------------------------------------
class EXCONFIG_PT_PatternMatch(bpy.types.Panel):
    bl_label = "ExConfig Pattern Match"
    bl_idname = "EXCONFIG_PT_pattern_match"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ExToolbox'
    bl_parent_id = "EXCONFIG_PT_panel"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 3

    def draw(self, context):
        layout = self.layout
        s = context.scene
        exconfig = s.exconfig

        box = layout.box()
        col = box.column(align=True)
        col.label(text="Variable Mapping", icon='CON_TRANSLIKE')
        
        # Only show if project is selected
        if exconfig.project_list == 'NONE':
            col.label(text="Select a project first", icon='INFO')
            return
        
        col.prop(exconfig, "pattern_match_source", text="Source")
        col.prop(exconfig, "pattern_match_target", text="Target")
        
        col.separator()
        col.operator("exconfig.generate_pattern_match", text="Generate Mapping", icon='LINKED')


def register():
    bpy.utils.register_class(EXCONFIG_PT_PatternMatch)


def unregister():
    bpy.utils.unregister_class(EXCONFIG_PT_PatternMatch)
