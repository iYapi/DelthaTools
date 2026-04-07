import bpy

class ImportVfxPlaneUI:
    def __init__(self, layout, context):
        self.layout = layout
        self.context = context

    def draw(self):
        layout = self.layout
        column = layout.column(align=True)
        column.label(text="Import VFX Plane:")
        column.operator("ivp.import_image_sequence", text="Import Image Sequence", icon='FILE_IMAGE')
        column.operator("ivp.import_movie_texture", text="Import Movie Texture", icon='FILE_MOVIE')