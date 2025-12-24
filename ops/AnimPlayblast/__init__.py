from . import add_safearea, apply_preset, render_playblast, control_camera, render_marker

modules = [
    control_camera,
    add_safearea,
    apply_preset,
    render_playblast,
    render_marker,
]


def register():
    for item in modules:
        item.register()


def unregister():
    for item in modules:
        item.unregister()
