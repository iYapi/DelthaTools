from . import subpanel, panel

modules = [panel, subpanel]


def register():
    for item in modules:
        item.register()


def unregister():
    for item in modules:
        item.unregister()
