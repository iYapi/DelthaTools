from . import check_missing_images

modules = [
    check_missing_images,
]


def register():
    for item in modules:
        item.register()


def unregister():
    for item in modules:
        item.unregister()
