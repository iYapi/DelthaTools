from . import import_img_seq_vfx, import_movie_vfx

modules = [import_img_seq_vfx, import_movie_vfx]

def register():
    for item in modules:
        item.register()
        
def unregister():
    for item in modules:
        item.unregister()