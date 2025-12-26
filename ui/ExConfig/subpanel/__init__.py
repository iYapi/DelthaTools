from . import basic, drive, pattern, pattern_match

modules = [
    basic,
    drive,
    pattern,
    pattern_match
]


def register():
    for item in modules:
        item.register()


def unregister():
    for item in modules:
        item.unregister()
