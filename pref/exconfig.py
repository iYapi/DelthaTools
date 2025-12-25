import bpy
import os
import json


# ------------------------------------------------------------------------
# ExConfig Properties
# ------------------------------------------------------------------------
def get_project_items(self, context):
    """Dynamic project list items"""
    items = [('NONE', "None", "No project selected")]
    
    # Try to load projects from config file
    config_path = os.path.join(bpy.utils.user_resource('CONFIG'), "exconfig.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            if "projects" in config_data:
                for project in config_data["projects"]:
                    name = project.get("name", "")
                    code = project.get("code", "")
                    if name:
                        # Use name as identifier and display
                        desc = f"Project: {name}" + (f" ({code})" if code else "")
                        items.append((name, name, desc))
        except Exception as e:
            print(f"Error loading project list: {e}")
    
    return items


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
    project_pattern_data: bpy.props.StringProperty(
        name="Pattern Data",
        description="JSON string containing the pattern data",
        default="{}",
    )
    project_write_mode: bpy.props.EnumProperty(
        name="Write Mode",
        description="Select the write mode for file operations",
        items=[
            ('APPEND', "Append", "Append to existing files"),
            ('OVERWRITE', "Overwrite", "Overwrite existing files"),
        ],
        default='APPEND',
    )
    project_list: bpy.props.EnumProperty(
        name="Project List",
        description="Select from available projects",
        items=get_project_items,
    )
    
    def get_pattern_dict(self):
        """Get pattern data as dictionary"""
        try:
            return json.loads(self.project_pattern_data)
        except:
            return {}
    
    def set_pattern_dict(self, pattern_dict):
        """Set pattern data from dictionary"""
        try:
            self.project_pattern_data = json.dumps(pattern_dict, ensure_ascii=False)
        except Exception as e:
            print(f"Error setting pattern data: {e}")


def register():
    bpy.utils.register_class(ExConfigProperties)
    bpy.types.Scene.exconfig = bpy.props.PointerProperty(type=ExConfigProperties)


def unregister():
    bpy.utils.unregister_class(ExConfigProperties)
    del bpy.types.Scene.exconfig
