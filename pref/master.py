import bpy


# ------------------------------------------------------------------------
# Navigation Properties
# ------------------------------------------------------------------------
class Toolbox(bpy.types.PropertyGroup):
    ui_mode: bpy.props.EnumProperty(
        name="Mode",
        description="Choose which tool page to display",
        items=[
            ('INFO', "Info", "Information about the addon"),
            ('LIGHTING_PROPERTIES', "LightingProperties", "Lighting override controls"),
            ('LIGHTING_SETUP', "LightingSetup", "Lighting setup tools"),
            ('ANIM_PLAYBLAST', "AnimPlayblast", "Animation playblast tools"),
        ],
        default='INFO',
    )
    json_config: bpy.props.StringProperty(
        name="JSON Config Path",
        default="/mnt/A/config_script/toolbox_config.json",
        subtype='FILE_PATH',
    )
    version: bpy.props.StringProperty(
        name="Version",
        default="0.1.15",
        options={'HIDDEN'}
    )

class ToolboxCompositing(bpy.types.PropertyGroup):
    ui_mode: bpy.props.EnumProperty(
        name="Mode",
        description="Choose which tool page to display",
        items=[
            ('INFO', "Info", "Information about the addon"),
            ('EYE_GLOW_COMPOSITING', "EyeGlowCompositing", "Eye glow compositing tools"),
        ],
        default='INFO',
    )


def register():
    bpy.utils.register_class(Toolbox)
    bpy.utils.register_class(ToolboxCompositing)
    bpy.types.Scene.toolbox = bpy.props.PointerProperty(type=Toolbox)
    bpy.types.Scene.toolbox_compositing = bpy.props.PointerProperty(type=ToolboxCompositing)


def unregister():
    bpy.utils.unregister_class(Toolbox)
    bpy.utils.unregister_class(ToolboxCompositing)
    del bpy.types.Scene.toolbox
    del bpy.types.Scene.toolbox_compositing
