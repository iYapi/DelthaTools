import os
import re
from pathlib import Path
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

    @staticmethod
    def get_latest_versioned_file(folder):
        # number immediately before the extension
        pattern = re.compile(r'(\d+)(?=\.[^.]+$)')
        latest_version = -1
        latest_file = None

        for path in Path(folder).iterdir():
            if not path.is_file():
                continue

            match = pattern.search(path.name)
            if not match:
                continue

            version = int(match.group(1))
            if version > latest_version:
                latest_version = version
                latest_file = path

        return latest_file

    @staticmethod
    def next_version_name(path):
        path = Path(path)

        # split once: name + extension
        stem = path.stem  # e.g. "project_v001"
        suffix = path.suffix  # e.g. ".blend"

        match = re.search(r'(.*?)(\d+)$', stem)
        if not match:
            raise ValueError("No version number found before file extension")

        prefix, version_str = match.groups()
        width = len(version_str)
        next_version = int(version_str) + 1

        new_name = f"{prefix}{next_version:0{width}d}{suffix}"
        return path.with_name(new_name)

    @staticmethod
    def remove_last_underscore(path):
        """
        Go up one folder and remove the last underscore-separated
        part of the filename.
        """
        path = Path(path)

        # go up one directory
        target_dir = path.parent.parent

        # remove last underscore chunk
        parts = path.stem.rsplit("_", 1)
        new_stem = parts[0] if len(parts) > 1 else path.stem

        return target_dir / f"{new_stem}{path.suffix}"

    @staticmethod
    def remove_trailing_number_from_last_underscore(path):
        """
        Remove trailing digits from the last underscore-separated
        token in the filename.
        """
        path = Path(path)

        # go up one directory
        target_dir = path.parent.parent

        stem = path.stem
        parts = stem.rsplit("_", 1)

        if len(parts) == 1:
            new_stem = re.sub(r'\d+$', '', stem)
        else:
            head, tail = parts
            tail = re.sub(r'\d+$', '', tail)
            new_stem = f"{head}_{tail}" if tail else head

        return target_dir / f"{new_stem}{path.suffix}"