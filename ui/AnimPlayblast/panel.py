import bpy

class AnimPlayblastUI:
    def __init__(self, layout, context):
        self.layout = layout
        self.context = context

    def draw(self):
        layout = self.layout
        s = self.context.scene

        column = layout.column(align=True)
        ## TODO: Select Project from prefs
        # row.prop(pref_props, "project", text="Project")
        column.label(text="Only work for BJL", icon='ERROR')
        column.operator("apb.apply_preset", text="Apply Preset", icon='PRESET')
        column.operator("apb.render_playblast", text="Render Playblast", icon='RENDER_ANIMATION')
        column.operator("apb.add_safe_area", text="Add Safe Area", icon='VIEW_CAMERA')
        layout.separator(factor=0.5)
        layout.label(text="Render Marker", icon='PMARKER_ACT')
        marker = layout.row(align=True)
        marker.operator("apb.start_render_marker", text="Start", icon='MARKER_HLT')
        marker.operator("apb.end_render_marker", text="End", icon='MARKER')
        layout.operator("apb.clear_render_markers", text="Clear Markers", icon='X')