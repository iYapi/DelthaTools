import bpy


class ImgWinPathUI:
    def __init__(self, layout, context):
        self.layout = layout
        self.context = context

    def draw(self):
        layout = self.layout

        column = layout.column(align=True)
        column.operator("iwp.check_missing_images", text="Fix Missing Images", icon='FILE_IMAGE')
