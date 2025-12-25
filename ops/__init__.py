from . import LightingProperties, LightingSetup, GraphNewWindow, EyeGlowCompositing, AnimPlayblast, ExConfig

modules = [
    ExConfig,
    LightingProperties,
    LightingSetup,
    GraphNewWindow,
    EyeGlowCompositing,
    AnimPlayblast
]


def register():
    for item in modules:
        item.register()


def unregister():
    for item in modules:
        item.unregister()
