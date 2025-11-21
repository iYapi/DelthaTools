from . import LightingProperties, LightingSetup, GraphNewWindow, EyeGlowCompositing

modules = [
    LightingProperties,
    LightingSetup,
    GraphNewWindow,
    EyeGlowCompositing
]


def register():
    for item in modules:
        item.register()


def unregister():
    for item in modules:
        item.unregister()
