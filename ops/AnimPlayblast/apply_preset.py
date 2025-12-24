import bpy
import json
import os
from ...utils.file_manager import FileManager

# ------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------

def load_playblast_preset(context, json_path=None, reporter=None):
    """Load and apply all settings from JSON using hasattr/setattr"""

    if json_path is None:
        reporter({'WARNING'}, f"No preset path provided.")
        return False

    try:
        with open(json_path, 'r') as f:
            preset = json.load(f)
    except FileNotFoundError:
        print(f"Preset not found: {json_path}")
        reporter({'WARNING'}, f"No preset path found.")
        return False

    scene = context.scene
    render = scene.render
    image_settings = render.image_settings
    ffmpeg = render.ffmpeg

    print("Applying playblast preset...")

    if "settings" not in preset:
        print("No settings found in preset")
        reporter({'WARNING'}, f"No settings found in preset.")
        return False

    # Apply all settings in a single loop
    for attr_name, value in preset["settings"].items():
        try:
            # Handle nested attributes (ffmpeg.*, image_settings.*)
            if "." in attr_name:
                obj_name, prop_name = attr_name.split(".")
                if obj_name == "ffmpeg":
                    obj = ffmpeg
                elif obj_name == "image_settings":
                    obj = image_settings
                else:
                    continue

                if hasattr(obj, prop_name):
                    setattr(obj, prop_name, value)

            # Handle render attributes
            elif hasattr(render, attr_name):
                # Handle color properties
                if attr_name in ["stamp_foreground", "stamp_background"]:
                    setattr(render, attr_name, tuple(value))
                else:
                    setattr(render, attr_name, value)

        except Exception as e:
            print(f"  Could not set {attr_name}: {e}")
            reporter({'WARNING'}, f"Could not set {attr_name}: {e}")

    print("Preset applied successfully!")
    reporter({'INFO'}, "Preset setting applied")
    return True


# ------------------------------------------------------------------------
# Apply Preset - Operator
# ------------------------------------------------------------------------
class APB_OT_ApplyPreset(bpy.types.Operator):
    bl_idname = "apb.apply_preset"
    bl_label = "Apply Preset"
    bl_description = "Apply the selected project preset"

    def execute(self, context):
        s = context.scene

        load_playblast_preset(context, json_path=s.toolbox.json_config, reporter=self.report)

        bpy.ops.apb.view_camera_operator()

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        # space.shading.type = 'MATERIAL'
                        space.shading.type = 'SOLID'
                        space.shading.color_type = 'TEXTURE'
                        break

        _, _, name, _ = FileManager.split_blend_filepath()
        s.render.stamp_note_text = name
        parts = [part for part in name.split("_") if part.strip()]

        print(parts)
        ## TODO: fix path preset
        letter = "".join(c for c in parts[4] if c.isalpha())
        dir_path = f"/mnt/A/Output/Playblast/{parts[0]}_0{int(parts[1][1:])}/{letter}"
        final_path = os.path.join(dir_path, f"{name}.mov")
        s.render.filepath = final_path

        self.report({'INFO'}, f"Preset applied successfully!")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(APB_OT_ApplyPreset)


def unregister():
    bpy.utils.unregister_class(APB_OT_ApplyPreset)
