import bpy

class AnimPlayblastUI:
    def __init__(self, layout, context):
        self.layout = layout
        self.context = context

    def draw(self):
        layout = self.layout
        s = self.context.scene

        row = layout.row(align=True)
        ## TODO: Select Project from prefs
        # row.prop(pref_props, "project", text="Project")
        layout.label(text="Only work for BJL", icon='ERROR')
        layout.operator("apb.apply_preset", text="Apply Preset", icon='PRESET')
        layout.operator("apb.render_playblast", text="Render Playblast", icon='RENDER_ANIMATION')
        layout.operator("apb.add_safe_area", text="Add Safe Area", icon='VIEW_CAMERA')