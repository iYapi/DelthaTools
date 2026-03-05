import bpy

class AssetColRenameUI:
    def __init__(self, layout, context):
        self.layout = layout
        self.context = context

    def draw(self):
        layout = self.layout
        layout.operator("acr.rename_append_asset", text="Append Asset Name")
        layout.operator("acr.rename_replace_asset", text="Replace Asset Name")