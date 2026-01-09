from . import navigation, ExConfig, ExLauncher


def register():
    navigation.register()
    ExConfig.register()
    ExLauncher.register()


def unregister():
    navigation.unregister()
    ExConfig.unregister()
    ExLauncher
