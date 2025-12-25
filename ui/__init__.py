from . import navigation, ExConfig


def register():
    navigation.register()
    ExConfig.register()


def unregister():
    navigation.unregister()
    ExConfig.unregister()
