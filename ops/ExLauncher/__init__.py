from . import save_master, save_progress

modules = [save_master, save_progress]


def register():
    for module in modules:
        module.register()


def unregister():
    for module in modules:
        module.unregister()
