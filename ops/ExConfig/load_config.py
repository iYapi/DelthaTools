import bpy
import os
from ...utils.json_manager import JSONManager


# ------------------------------------------------------------------------
# Helper function to load project data into properties
# ------------------------------------------------------------------------
def load_project_data(exconfig, project_data, pattern_name=None):
    """Load project data into ExConfig properties
    
    Args:
        exconfig: ExConfig property group
        project_data: Project dictionary from config
        pattern_name: Optional specific pattern to load. If None, uses selected pattern or first available.
    """
    # Load basic data
    exconfig.project_name = project_data.get("name", "")
    exconfig.project_code = project_data.get("code", "")
    
    # Load drive data
    drive_data = project_data.get("path", {}).get("drive", {})
    exconfig.project_drive_prod = drive_data.get("production", "")
    exconfig.project_drive_output = drive_data.get("output", "")

    # Load pattern data
    patterns_data = project_data.get("path", {}).get("patterns", {})
    if patterns_data:
        # Determine which pattern to load
        selected_pattern_name = pattern_name
        
        # If no pattern specified, try to use the selected pattern from UI
        if not selected_pattern_name:
            if exconfig.project_pattern_selected != 'NONE':
                selected_pattern_name = exconfig.project_pattern_selected
        
        # If still no pattern, use first available
        if not selected_pattern_name or selected_pattern_name not in patterns_data:
            selected_pattern_name = next(iter(patterns_data.keys()), None)
        
        if selected_pattern_name and selected_pattern_name in patterns_data:
            pattern = patterns_data[selected_pattern_name]
            
            # Map pattern name to enum
            pattern_map = {
                'None': 'NONE',
                'Animation': 'ANIM',
                'Compositing': 'COMP',
                'Playblast': 'PLAYBLAST'
            }
            exconfig.project_pattern_division = pattern_map.get(selected_pattern_name, 'NONE')
            
            # Set the pattern name field
            exconfig.project_pattern_name = selected_pattern_name
            
            exconfig.project_pattern_base = pattern.get("base_path", "")
            exconfig.project_pattern_example = pattern.get("example_path", "")
            
            # Save full pattern data to preferences
            exconfig.set_pattern_dict(pattern)
            
            return selected_pattern_name
    
    return None


# ------------------------------------------------------------------------
# ExConfig Load From File - Operator (File Browser)
# ------------------------------------------------------------------------
class EXCONFIG_OT_LoadConfigFile(bpy.types.Operator):
    bl_idname = "exconfig.load_config_file"
    bl_label = "Browse Config File"
    bl_description = "Browse and load ExConfig settings from a file"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Path to the config file",
        subtype='FILE_PATH',
    )

    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={'HIDDEN'},
    )

    def execute(self, context):
        if not self.filepath:
            self.report({'ERROR'}, "No file selected")
            return {'CANCELLED'}

        # Load config file
        config_data = JSONManager.load_json(self.filepath)
        
        if not config_data:
            self.report({'ERROR'}, "Failed to load config file")
            return {'CANCELLED'}

        if "projects" not in config_data or not config_data["projects"]:
            self.report({'ERROR'}, "No projects found in config file")
            return {'CANCELLED'}

        # Get the selected project from project_list or use first project
        s = context.scene
        exconfig = s.exconfig
        
        # Find selected project or use first
        selected_project = None
        if exconfig.project_list != 'NONE':
            for project in config_data["projects"]:
                if project.get("name") == exconfig.project_list:
                    selected_project = project
                    break
        
        if not selected_project:
            selected_project = config_data["projects"][0]

        # Load project data into properties
        pattern_name = load_project_data(exconfig, selected_project)
        
        message = f"Config loaded: {selected_project.get('name', 'Unknown')}"
        if pattern_name:
            message += f" - Pattern: {pattern_name}"
        self.report({'INFO'}, message)
        return {'FINISHED'}

    def invoke(self, context, event):
        # Set default path to config directory
        default_path = os.path.join(bpy.utils.user_resource('CONFIG'), "exconfig.json")
        if os.path.exists(default_path):
            self.filepath = default_path
        
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


# ------------------------------------------------------------------------
# ExConfig Load Selected Project - Operator (From Dropdown)
# ------------------------------------------------------------------------
class EXCONFIG_OT_LoadSelectedProject(bpy.types.Operator):
    bl_idname = "exconfig.load_selected_project"
    bl_label = "Load Selected Project"
    bl_description = "Load the selected project from the dropdown list"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        s = context.scene
        exconfig = s.exconfig
        
        # Check if a project is selected
        if exconfig.project_list == 'NONE':
            self.report({'WARNING'}, "No project selected")
            return {'CANCELLED'}
        
        # Load config file
        config_path = os.path.join(bpy.utils.user_resource('CONFIG'), "exconfig.json")
        if not os.path.exists(config_path):
            self.report({'ERROR'}, "Config file not found")
            return {'CANCELLED'}
        
        config_data = JSONManager.load_json(config_path)
        
        if not config_data:
            self.report({'ERROR'}, "Failed to load config file")
            return {'CANCELLED'}

        if "projects" not in config_data or not config_data["projects"]:
            self.report({'ERROR'}, "No projects found in config file")
            return {'CANCELLED'}
        
        # Find the selected project
        selected_project = None
        for project in config_data["projects"]:
            if project.get("name") == exconfig.project_list:
                selected_project = project
                break
        
        if not selected_project:
            self.report({'ERROR'}, f"Project '{exconfig.project_list}' not found")
            return {'CANCELLED'}
        
        # Load project data into properties
        pattern_name = load_project_data(exconfig, selected_project)
        
        message = f"Loaded project: {exconfig.project_list}"
        if pattern_name:
            message += f" - Pattern: {pattern_name}"
        self.report({'INFO'}, message)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(EXCONFIG_OT_LoadConfigFile)
    bpy.utils.register_class(EXCONFIG_OT_LoadSelectedProject)


def unregister():
    bpy.utils.unregister_class(EXCONFIG_OT_LoadSelectedProject)
    bpy.utils.unregister_class(EXCONFIG_OT_LoadConfigFile)
