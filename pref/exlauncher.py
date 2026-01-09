import bpy


# ------------------------------------------------------------------------
# ExLauncher Properties
# ------------------------------------------------------------------------
class ExLauncherProperties(bpy.types.PropertyGroup):
    version_type: bpy.props.EnumProperty(
        name="Version Type",
        description="Choose the type of version increment",
        items=[
            ('LAST_NUMBER', "Last Number", "Increment the last number in the last underscore segment"),
            ('LAST_UNDERSCORE', "Last Underscore", "Increment the entire last underscore segment"),
        ],
        default='LAST_NUMBER'
    )


def register():
    bpy.utils.register_class(ExLauncherProperties)
    bpy.types.Scene.exlauncher = bpy.props.PointerProperty(type=ExLauncherProperties)


def unregister():
    bpy.utils.unregister_class(ExLauncherProperties)
    del bpy.types.Scene.exlauncher
