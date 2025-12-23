import os
from .constants import ADDON_DIR


# ------------------------------------------------------------------------
# File Manager
# ------------------------------------------------------------------------
class FileManager:
    @staticmethod
    def get_addon_directory():
        return ADDON_DIR

    @staticmethod
    def get_filepath(filename):
        addon_dir = FileManager.get_addon_directory()
        return os.path.join(addon_dir, filename)

    @staticmethod
    def split_blend_filepath(fp: str | None = None) -> tuple[str, str, str, str]:
        if fp is None:
            import bpy
            fp = bpy.data.filepath or ""

        if not fp:
            return ("", "Untitled.blend", "Untitled", ".blend")

        from pathlib import Path
        p = Path(fp)
        return (str(p.parent), p.name, p.stem, p.suffix)