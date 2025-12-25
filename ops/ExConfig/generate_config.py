import bpy
import os
from ...utils.path_analyzer import PathAnalyzer
from ...utils.json_manager import JSONManager
from dataclasses import asdict


# ------------------------------------------------------------------------
# ExConfig Generate - Operator
# ------------------------------------------------------------------------
class EXCONFIG_OT_GenerateConfig(bpy.types.Operator):
    bl_idname = "exconfig.generate_config"
    bl_label = "Generate ExConfig"
    bl_description = "Generate ExConfig settings for MasterX Tools"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        s = context.scene
        exconfig = s.exconfig

        # Validate inputs
        if not exconfig.project_name:
            self.report({'ERROR'}, "Project name is required")
            return {'CANCELLED'}

        if not exconfig.project_pattern_base:
            self.report({'ERROR'}, "Base path is required")
            return {'CANCELLED'}

        if not exconfig.project_pattern_example:
            self.report({'ERROR'}, "Example path is required")
            return {'CANCELLED'}

        # Map enum value to label for pattern name
        division_map = {
            'NONE': 'None',
            'ANIM': 'Animation',
            'COMP': 'Compositing'
        }
        pattern_name = division_map.get(exconfig.project_pattern_division, exconfig.project_pattern_division)

        # Create pattern using PathAnalyzer
        analyzer = PathAnalyzer()
        try:
            pattern = analyzer.create_pattern(
                name=pattern_name,
                base_path=exconfig.project_pattern_base,
                full_path=exconfig.project_pattern_example,
                save_example=True
            )
        except ValueError as e:
            self.report({'ERROR'}, f"Pattern creation failed: {str(e)}")
            return {'CANCELLED'}

        # Convert PathPattern dataclass to dict
        pattern_dict = asdict(pattern)

        # Add full_pattern
        analyzer.patterns[pattern.name] = pattern
        pattern_dict["full_pattern"] = analyzer.get_full_pattern_string(pattern.name)

        # Build the config structure matching config.example.json
        # Check if config already exists to append or overwrite
        config_path = os.path.join(bpy.utils.user_resource('CONFIG'), "exconfig.json")
        existing_projects = []
        
        # Load existing config if it exists and mode is APPEND
        if exconfig.project_write_mode == 'APPEND' and os.path.exists(config_path):
            existing_config = JSONManager.load_json(config_path)
            if existing_config and "projects" in existing_config:
                # Filter out project with same name to avoid duplicates
                existing_projects = [p for p in existing_config["projects"] if p.get("name") != exconfig.project_name]
        
        # Create new project entry
        new_project = {
            "name": exconfig.project_name,
            "code": exconfig.project_code if exconfig.project_code else "",
            "path": {
                "drive": {
                    "production": exconfig.project_drive_prod if exconfig.project_drive_prod else "",
                    "output": exconfig.project_drive_output if exconfig.project_drive_output else "",
                },
                "patterns": {
                    pattern.name: pattern_dict
                }
            }
        }
        
        # Add new project to list
        existing_projects.append(new_project)
        
        # Build final config structure
        data = {
            "projects": existing_projects
        }
        
        # Save to config file
        JSONManager.save_json(data, config_path)
        
        print(f"Config saved to: {config_path}")
        print(data)
        self.report({'INFO'}, f"ExConfig saved to {config_path}")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(EXCONFIG_OT_GenerateConfig)


def unregister():
    bpy.utils.unregister_class(EXCONFIG_OT_GenerateConfig)
