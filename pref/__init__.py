from . import master, exconfig, lighting_properties, lighting_setup, exlauncher, proxyfy

modules = [
    master,
    exconfig,
    exlauncher,
    lighting_properties,
    lighting_setup,
    proxyfy,
]


def register():
    for item in modules:
        item.register()


def unregister():
    for item in modules:
        item.unregister()
