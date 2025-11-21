import bpy

class EyeGlowCompositingUI:
    def __init__(self, layout, context):
        self.layout = layout
        self.context = context

    def draw(self):
        layout = self.layout
        s = self.context.scene

        row_func = layout.row(align=True)
        row_func.operator("egc.append_blend", text="Setup Eye Glow", icon="NODE_COMPOSITING")