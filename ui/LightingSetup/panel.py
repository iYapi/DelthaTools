import bpy

class LightingSetupUI:
    def __init__(self, layout, context):
        self.layout = layout
        self.context = context

    def draw(self):
        layout = self.layout
        s = self.context.scene
        props = s.lighting_setup

        col_func = layout.column(align=True)
        col_func.prop(props, "lighting_type", text="Lighting Type", expand=False)
        col_func.operator("bls.append_blend", text="Append Setup", icon="IMPORT")

