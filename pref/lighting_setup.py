import bpy


# ------------------------------------------------------------------------
# Lighting Setup - Append Blend File
# ------------------------------------------------------------------------
class LIGHTINGSETUP(bpy.types.PropertyGroup):
    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Path to the blend file to append from",
        default="presets/blend/scene_presets.blend",
        subtype="FILE_PATH",
    )
    lighting_type: bpy.props.EnumProperty(
        name="Lighting Type",
        description="Setup lighting presets",
        items=[
            ("LIGHTCHAR", "LightChar", "2 area light rim & fill"),
            ("SPLITKEY", "SplitKey", "Global key light"),
            ("ASSETBASE", "AssetBase", "Asset base scene"),
        ],
        default="LIGHTCHAR",
    )


def register():
    bpy.utils.register_class(LIGHTINGSETUP)
    bpy.types.Scene.lighting_setup = bpy.props.PointerProperty(type=LIGHTINGSETUP)


def unregister():
    bpy.utils.unregister_class(LIGHTINGSETUP)
    del bpy.types.Scene.lighting_setup
