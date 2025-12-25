import bpy
import os
from ...utils.path_analyzer import PathAnalyzer
from ...utils.config_manager import ConfigManager
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
        config_manager = ConfigManager()
        data = config_manager.get_project_dict_no_pattern(exconfig.project_name, exconfig.project_code,
                                                          exconfig.project_drive_prod, exconfig.project_drive_output)
        data["patterns"] = {pattern.name: pattern_dict}

        config_path = os.path.join(bpy.utils.user_resource('CONFIG'), "exconfig.json")
        JSONManager().save_json(data=data, filepath=config_path)
        print(data)
        self.report({'INFO'}, "ExConfig generated successfully.")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(EXCONFIG_OT_GenerateConfig)


def unregister():
    bpy.utils.unregister_class(EXCONFIG_OT_GenerateConfig)
