from . import generate_config, load_config, pattern_match

modules = [
    generate_config,
    load_config,
    pattern_match,
]


def register():
    for item in modules:
        item.register()


def unregister():
    for item in modules:
        item.unregister()
