import bpy

class ExConfigPanelUI:
    def __init__(self, layout, context):
        self.layout = layout
        self.context = context

    def draw(self):
        layout = self.layout
        s = self.context.scene

        box = layout.box()
        box.label(text="ExToolbox Configuration", icon="PREFERENCES")

        row = box.row(align=True)
        row.prop(s.toolbox, "show_exconfig", text="Show Config")