import bpy
import os


def safe_abspath(p: str) -> str:
    """Safely convert to absolute path."""
    if not p:
        return ""
    try:
        return bpy.path.abspath(p)
    except Exception:
        return p


def exists(p: str) -> bool:
    """Check if path exists."""
    return bool(p) and os.path.exists(os.path.normpath(p))


class IWP_OT_CheckMissingImages(bpy.types.Operator):
    bl_idname = "iwp.check_missing_images"
    bl_label = "Check Missing Images"
    bl_description = "Check for missing image paths and attempt to fix them"
    bl_options = {'REGISTER', 'UNDO'}

    only_used: bpy.props.BoolProperty(
        name="Only Used Images",
        description="Only check images with users > 0",
        default=True
    )

    def execute(self, context):
        missing_found = False
        missing_images = []

        # Check for missing images
        for img in bpy.data.images:
            if self.only_used and img.users == 0:
                continue

            # Get raw path
            raw = (img.filepath_raw or img.filepath or "").strip()
            if not raw:
                continue

            # If packed, not missing
            if img.packed_file is not None:
                continue

            missing = False
            # UDIM / TILED
            if img.source == 'TILED' and "<UDIM>" in raw:
                # Missing if all registered tiles not found
                found_any = False
                for tile in img.tiles:
                    tile_path = safe_abspath(raw.replace("<UDIM>", str(tile.number)))
                    if exists(tile_path):
                        found_any = True
                        break
                missing = (not found_any)
            else:
                # Non-UDIM
                missing = (not exists(safe_abspath(raw)))

            if missing:
                if not missing_found:
                    print("MISSING_IMAGES_FOUND")
                    missing_found = True
                print(f"- {img.name} | path='{raw}'")
                missing_images.append(img)

        # If missing images found, create backup and try to fix paths
        if missing_found:
            # Get blend file path
            blend_path = bpy.data.filepath
            if not blend_path:
                self.report({'ERROR'}, "Please save the blend file first")
                return {'CANCELLED'}

            # Try to fix paths (replace A:\\ with /mnt/A/)
            fixed_count = 0
            for img in missing_images:
                old_path = img.filepath
                if "A:\\\\" in old_path or "A:/" in old_path:
                    new_path = old_path.replace("A:\\\\", "/mnt/A/").replace("A:/", "/mnt/A/")
                    img.filepath = new_path
                    fixed_count += 1
                    print(f"FIXED_PATH: {img.name}")

            self.report({'INFO'}, f"Found {len(missing_images)} missing images. Fixed {fixed_count} paths.")
            return {'FINISHED'}
        else:
            self.report({'INFO'}, "No missing images found")
            return {'FINISHED'}


def register():
    bpy.utils.register_class(IWP_OT_CheckMissingImages)


def unregister():
    bpy.utils.unregister_class(IWP_OT_CheckMissingImages)
