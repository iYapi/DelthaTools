from . import panel

modules = [panel]


def register():
    for item in modules:
        item.register()


def unregister():
    for item in modules:
        item.unregister()
