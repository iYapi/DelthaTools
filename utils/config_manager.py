import bpy
import os
import json


# ------------------------------------------------------------------------
# Config Manager
# ------------------------------------------------------------------------
class ConfigManager:
    @staticmethod
    def get_project_dict_no_pattern(project_name: str, project_code: str, project_drive_prod: str, project_drive_output: str) -> dict:
        data = {
            "name": project_name,
            "code": project_code if project_code else "",
            "path": {
                "drive": {
                    "production": project_drive_prod if project_drive_prod else "",
                    "output": project_drive_output if project_drive_output else "",
                }
            }
        }
        return data
    
    @staticmethod
    def get_pattern_from_config(project_name: str, pattern_name: str) -> dict:
        """
        Get a specific pattern from a project in the config file.
        
        Args:
            project_name: Name of the project (e.g., "Jagat")
            pattern_name: Name of the pattern (e.g., "Animation", "Compositing", "Playblast")
        
        Returns:
            dict: Pattern data or None if not found
        
        Example:
            pattern = ConfigManager.get_pattern_from_config("Jagat", "Animation")
            if pattern:
                base_path = pattern.get("base_path")
                example_path = pattern.get("example_path")
        """
        config_path = os.path.join(bpy.utils.user_resource('CONFIG'), "exconfig.json")
        
        if not os.path.exists(config_path):
            print(f"Config file not found: {config_path}")
            return None
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Find the project
            if "projects" not in config_data:
                print("No projects found in config")
                return None
            
            for project in config_data["projects"]:
                if project.get("name") == project_name:
                    # Get patterns
                    patterns = project.get("path", {}).get("patterns", {})
                    if pattern_name in patterns:
                        return patterns[pattern_name]
                    else:
                        print(f"Pattern '{pattern_name}' not found in project '{project_name}'")
                        available = list(patterns.keys())
                        print(f"Available patterns: {available}")
                        return None
            
            print(f"Project '{project_name}' not found in config")
            return None
            
        except Exception as e:
            print(f"Error loading pattern from config: {e}")
            return None
    
    @staticmethod
    def get_current_project_pattern(pattern_name: str = None) -> dict:
        """
        Get a pattern from the currently selected project in ExConfig.
        
        Args:
            pattern_name: Name of the pattern to get. If None, uses currently selected pattern.
        
        Returns:
            dict: Pattern data or None if not found
        
        Example:
            # Get currently selected pattern
            pattern = ConfigManager.get_current_project_pattern()
            
            # Get specific pattern from current project
            pattern = ConfigManager.get_current_project_pattern("Animation")
        """
        try:
            exconfig = bpy.context.scene.exconfig
            
            # Get current project name
            project_name = exconfig.project_list
            if project_name == 'NONE':
                print("No project selected in ExConfig")
                return None
            
            # Determine pattern name
            if pattern_name is None:
                # Use selected pattern
                pattern_name = exconfig.project_pattern_selected
                if pattern_name == 'NONE':
                    print("No pattern selected in ExConfig")
                    return None
            
            # Get pattern from config
            return ConfigManager.get_pattern_from_config(project_name, pattern_name)
            
        except Exception as e:
            print(f"Error getting current project pattern: {e}")
            return None
