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


def get_pattern_items(self, context):
    """Dynamic pattern list items for selected project"""
    items = [('NONE', "None", "No pattern selected")]
    
    # Get selected project
    exconfig = context.scene.exconfig
    selected_project = exconfig.project_list
    
    if selected_project == 'NONE':
        return items
    
    # Try to load patterns from config file
    config_path = os.path.join(bpy.utils.user_resource('CONFIG'), "exconfig.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            if "projects" in config_data:
                for project in config_data["projects"]:
                    if project.get("name") == selected_project:
                        patterns = project.get("path", {}).get("patterns", {})
                        for pattern_name in patterns.keys():
                            items.append((pattern_name, pattern_name, f"Pattern: {pattern_name}"))
                        break
        except Exception as e:
            print(f"Error loading pattern list: {e}")
    
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
            ('PLAYBLAST', "Playblast", "Settings Playblast"),
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
    project_pattern_selected: bpy.props.EnumProperty(
        name="Pattern Selection",
        description="Select pattern to load/save",
        items=get_pattern_items,
    )
    
    # Pattern matching properties
    pattern_match_source: bpy.props.EnumProperty(
        name="Source Pattern",
        description="Source pattern (e.g., Animation)",
        items=get_pattern_items,
    )
    pattern_match_target: bpy.props.EnumProperty(
        name="Target Pattern",
        description="Target pattern (e.g., Playblast)",
        items=get_pattern_items,
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
