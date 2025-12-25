from . import generate_config, load_config

modules = [
    generate_config,
    load_config,
]


def register():
    for item in modules:
        item.register()


def unregister():
    for item in modules:
        item.unregister()
