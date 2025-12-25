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
