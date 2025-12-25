import bpy
import os
from ...utils.json_manager import JSONManager


# ------------------------------------------------------------------------
# ExConfig Load - Operator
# ------------------------------------------------------------------------
class EXCONFIG_OT_LoadConfig(bpy.types.Operator):
    bl_idname = "exconfig.load_config"
    bl_label = "Load ExConfig"
    bl_description = "Load ExConfig settings from file"
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
        exconfig.project_name = selected_project.get("name", "")
        exconfig.project_code = selected_project.get("code", "")
        
        # Load drive data
        drive_data = selected_project.get("path", {}).get("drive", {})
        exconfig.project_drive_prod = drive_data.get("production", "")
        exconfig.project_drive_output = drive_data.get("output", "")

        # Load pattern data (use first pattern found)
        patterns_data = selected_project.get("path", {}).get("patterns", {})
        if patterns_data:
            # Get first pattern
            first_pattern_name = next(iter(patterns_data.keys()), None)
            if first_pattern_name:
                pattern = patterns_data[first_pattern_name]
                
                # Map pattern name to enum
                pattern_map = {
                    'None': 'NONE',
                    'Animation': 'ANIM',
                    'Compositing': 'COMP'
                }
                exconfig.project_pattern_division = pattern_map.get(first_pattern_name, 'NONE')
                
                exconfig.project_pattern_base = pattern.get("base_path", "")
                exconfig.project_pattern_example = pattern.get("example_path", "")

        self.report({'INFO'}, f"Config loaded: {selected_project.get('name', 'Unknown')}")
        return {'FINISHED'}

    def invoke(self, context, event):
        # Set default path to config directory
        default_path = os.path.join(bpy.utils.user_resource('CONFIG'), "exconfig.json")
        if os.path.exists(default_path):
            self.filepath = default_path
        
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


def register():
    bpy.utils.register_class(EXCONFIG_OT_LoadConfig)


def unregister():
    bpy.utils.unregister_class(EXCONFIG_OT_LoadConfig)
