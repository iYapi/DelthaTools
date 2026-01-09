from . import LightingProperties, LightingSetup, GraphNewWindow, EyeGlowCompositing, AnimPlayblast, ExConfig, \
    ImgWinPath, ExLauncher

modules = [
    ExConfig,
    ExLauncher,
    LightingProperties,
    LightingSetup,
    GraphNewWindow,
    EyeGlowCompositing,
    AnimPlayblast,
    ImgWinPath
]


def register():
    for item in modules:
        item.register()


def unregister():
    for item in modules:
        item.unregister()
