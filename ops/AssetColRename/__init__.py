from . import rename_append_asset, rename_replace_asset

modules = [
    rename_append_asset,
    rename_replace_asset,
]

def register():
    for item in modules:
        item.register()


def unregister():
    for item in modules:
        item.unregister()