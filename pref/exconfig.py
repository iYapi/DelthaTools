import bpy


# ------------------------------------------------------------------------
# ExConfig Properties
# ------------------------------------------------------------------------
class ExConfigProperties(bpy.types.PropertyGroup):
    project_name: bpy.props.StringProperty(
        name="Project Name",
        default="",
    )
    project_code: bpy.props.StringProperty(
        name="Project Code",
        default="",
    )
    project_drive_prod: bpy.props.StringProperty(
        name="Production Drive",
        default="",
        maxlen=1
    )
    project_drive_output: bpy.props.StringProperty(
        name="Output Drive",
        default="",
        maxlen=1
    )
    project_pattern_division: bpy.props.EnumProperty(
        name="Division Pattern",
        description="Select the division pattern",
        items=[
            ('NONE', "None", "Settings None"),
            ('ANIM', "Animation", "Settings Animation"),
            ('COMP', "Compositing", "Settings Compositing"),
        ],
        default='NONE',
    )
    project_pattern_name: bpy.props.StringProperty(
        name="Name Pattern",
        default="",
    )
    project_pattern_base: bpy.props.StringProperty(
        name="Base Pattern",
        default="",
        subtype='DIR_PATH',
    )
    project_pattern_example: bpy.props.StringProperty(
        name="Example Pattern",
        default="",
        subtype='DIR_PATH',
    )


def register():
    bpy.utils.register_class(ExConfigProperties)
    bpy.types.Scene.exconfig = bpy.props.PointerProperty(type=ExConfigProperties)


def unregister():
    bpy.utils.unregister_class(ExConfigProperties)
    del bpy.types.Scene.exconfig
