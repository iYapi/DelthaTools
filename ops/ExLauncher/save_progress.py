import bpy
from pathlib import Path
from ...utils.file_manager import FileManager


# ------------------------------------------------------------------------
# Save Progress Operator
# ------------------------------------------------------------------------
class EXLAUNCHER_OT_SaveProgress(bpy.types.Operator):
    bl_idname = "exlauncher.save_progress"
    bl_label = "Save Progress"
    bl_description = "Save current progress in ExLauncher"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not bpy.data.filepath:
            self.report({'ERROR'}, "Please save the Blender file before saving progress.")
            return {'CANCELLED'}

        project_path = Path(bpy.data.filepath)
        project_dir = project_path.parent

        latest_file = FileManager.get_latest_versioned_file(project_dir)

        if not latest_file:
            self.report({'ERROR'}, "No versioned .blend files found.")
            return {'CANCELLED'}

        next_path = FileManager.next_version_name(latest_file)

        bpy.ops.wm.save_as_mainfile(filepath=str(next_path))

        self.report({'INFO'}, f"Progress saved for project '{next_path}'")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(EXLAUNCHER_OT_SaveProgress)


def unregister():
    bpy.utils.unregister_class(EXLAUNCHER_OT_SaveProgress)
