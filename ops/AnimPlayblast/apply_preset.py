import bpy
import json
import os
from ...utils.file_manager import FileManager
from ...utils.config_manager import ConfigManager
from ...utils.path_analyzer import PathAnalyzer

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
        exconfig = s.exconfig
        
        # Get playblast config path from exconfig
        json_path = exconfig.playblast_config
        
        if not json_path:
            self.report({'ERROR'}, "No playblast config path set. Please set it in ExConfig > Playblast Config panel.")
            return {'CANCELLED'}
        
        if not os.path.exists(json_path):
            self.report({'ERROR'}, f"Playblast config file not found: {json_path}")
            return {'CANCELLED'}

        load_playblast_preset(context, json_path=json_path, reporter=self.report)

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

        print("=" * 60)
        print("AnimPlayblast - Generating Output Path")
        print("=" * 60)
        
        # Get Animation pattern to extract variables from blend file path
        animation_pattern = ConfigManager.get_current_project_pattern("Animation")
        # Get Playblast pattern to build output path
        playblast_pattern = ConfigManager.get_current_project_pattern("Playblast")
        
        if animation_pattern and playblast_pattern:
            # Get the full blend file path
            blend_path = bpy.data.filepath
            
            if blend_path:
                try:
                    # Step 1: Extract variables from Animation pattern
                    analyzer = PathAnalyzer()
                    analyzer.load_from_dict({"patterns": {"Animation": animation_pattern, "Playblast": playblast_pattern}})
                    
                    print(f"Blend file path: {blend_path}")
                    variables = analyzer.extract_variables("Animation", blend_path)
                    print(f"Extracted variables from Animation pattern: {variables}")
                    
                    # Step 2: Get pattern match if available
                    exconfig = s.exconfig
                    project_name = exconfig.project_list
                    match_name = "animation_playblast"
                    pattern_match = ConfigManager.get_pattern_match(project_name, match_name)
                    
                    # Step 3: Build output path using Playblast pattern with pattern matching
                    if pattern_match:
                        print(f"Using pattern match '{match_name}': {pattern_match}")
                        pattern_matches = {match_name: pattern_match}
                        output_path = analyzer.build_path("Playblast", variables, match=match_name, pattern_matches=pattern_matches)
                        print(f"Built path with pattern matching")
                    else:
                        print("WARNING: No pattern match found!")
                        print("Please create pattern match in ExConfig > Pattern Match panel")
                        print("Using direct variable mapping (may not work correctly)")
                        output_path = analyzer.build_path("Playblast", variables)
                    
                    # Check if output path already has correct extension
                    playblast_ext = playblast_pattern.get("file_extension", ".mov")
                    if not output_path.endswith(playblast_ext):
                        # Ensure it has correct extension
                        output_path = os.path.splitext(output_path)[0] + playblast_ext
                    
                    s.render.filepath = output_path
                    print(f"✓ Playblast output path: {output_path}")
                    print("=" * 60)
                    
                except Exception as e:
                    print(f"Error building path from patterns: {e}")
                    import traceback
                    traceback.print_exc()
                    print("=" * 60)
                    print("ERROR: Failed to generate playblast output path")
                    print("Please check your ExConfig pattern configuration:")
                    print("  1. Ensure Animation pattern is correctly configured")
                    print("  2. Ensure Playblast pattern is correctly configured")
                    print("  3. Generate pattern match in ExConfig > Pattern Match panel")
                    print("=" * 60)
                    self.report({'ERROR'}, "Failed to generate output path. Check console for details.")
                    return {'CANCELLED'}
            else:
                print("=" * 60)
                print("ERROR: Blend file not saved")
                print("Please save the blend file before using AnimPlayblast")
                print("The Animation pattern needs a file path to extract variables from")
                print("=" * 60)
                self.report({'ERROR'}, "Blend file not saved. Save the file first.")
                return {'CANCELLED'}
        else:
            print("=" * 60)
            print("ERROR: Required patterns not configured in ExConfig")
            if not animation_pattern:
                print("  - Animation pattern not found")
            if not playblast_pattern:
                print("  - Playblast pattern not found")
            print("Please configure both patterns in ExConfig panel")
            print("=" * 60)
            self.report({'ERROR'}, "Animation and/or Playblast patterns not configured.")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Preset applied successfully!")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(APB_OT_ApplyPreset)


def unregister():
    bpy.utils.unregister_class(APB_OT_ApplyPreset)
