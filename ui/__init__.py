from . import navigation, ExConfig, ExLauncher


def register():
    ExLauncher.register()
    navigation.register()
    ExConfig.register()


def unregister():
    ExLauncher.unregister()
    navigation.unregister()
    ExConfig.unregister()
