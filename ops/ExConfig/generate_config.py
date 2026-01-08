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

        # Get pattern name from the enum's display text
        # This retrieves the second element (display name) from the enum items
        pattern_name = None
        for item in exconfig.bl_rna.properties['project_pattern_division'].enum_items:
            if item.identifier == exconfig.project_pattern_division:
                pattern_name = item.name
                break
        
        if not pattern_name or pattern_name == 'None':
            self.report({'ERROR'}, "Please select a pattern type (Animation, Compositing, or Playblast)")
            return {'CANCELLED'}

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
        
        # Save pattern data to preferences as JSON string
        exconfig.set_pattern_dict(pattern_dict)

        # Build the config structure matching config.example.json
        # Check if config already exists to append or overwrite
        config_path = os.path.join(bpy.utils.user_resource('CONFIG'), "exconfig.json")
        existing_projects = []
        project_exists = False
        existing_patterns = {}
        
        # Load existing config if it exists
        if os.path.exists(config_path):
            existing_config = JSONManager.load_json(config_path)
            if existing_config and "projects" in existing_config:
                if exconfig.project_write_mode == 'APPEND':
                    # In APPEND mode, keep all projects and merge patterns for matching project
                    for p in existing_config["projects"]:
                        if p.get("name") == exconfig.project_name:
                            project_exists = True
                            # Save existing patterns to merge with new one
                            existing_patterns = p.get("path", {}).get("patterns", {})
                            # Preserve existing playblast_config if not changed
                            if not exconfig.playblast_config and "playblast_config" in p:
                                exconfig.playblast_config = p.get("playblast_config", "")
                        else:
                            # Keep other projects as-is
                            existing_projects.append(p)
                # In OVERWRITE mode, existing_projects stays empty (replace entire file)
        
        # Merge new pattern with existing patterns
        merged_patterns = existing_patterns.copy()
        merged_patterns[pattern.name] = pattern_dict
        
        # Create new project entry with merged patterns
        new_project = {
            "name": exconfig.project_name,
            "code": exconfig.project_code if exconfig.project_code else "",
            "path": {
                "drive": {
                    "production": exconfig.project_drive_prod if exconfig.project_drive_prod else "",
                    "output": exconfig.project_drive_output if exconfig.project_drive_output else "",
                },
                "patterns": merged_patterns
            }
        }
        
        # Add playblast_config if set
        if exconfig.playblast_config:
            new_project["playblast_config"] = exconfig.playblast_config
        
        # Add new project to list
        existing_projects.append(new_project)
        
        # Build final config structure
        data = {
            "projects": existing_projects
        }
        
        # Save to config file
        try:
            JSONManager.save_json(data, config_path)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to save config: {str(e)}")
            return {'CANCELLED'}
        
        # Report result
        pattern_count = len(merged_patterns)
        if exconfig.project_write_mode == 'OVERWRITE':
            message = f"Config saved (OVERWRITE): {exconfig.project_name} with {pattern_count} pattern(s)"
        elif project_exists:
            message = f"Config updated: {exconfig.project_name} - Pattern '{pattern.name}' saved ({pattern_count} total)"
        else:
            message = f"Config added: {exconfig.project_name} - Pattern '{pattern.name}' saved"
        
        print(f"Config saved to: {config_path}")
        print(data)
        self.report({'INFO'}, message)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(EXCONFIG_OT_GenerateConfig)


def unregister():
    bpy.utils.unregister_class(EXCONFIG_OT_GenerateConfig)
