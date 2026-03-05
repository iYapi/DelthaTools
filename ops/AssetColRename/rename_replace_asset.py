import bpy

class ACR_OT_RenameReplaceAsset(bpy.types.Operator):
    """Rename Replace Asset"""
    bl_idname = "acr.rename_replace_asset"
    bl_label = "Rename Replace Asset"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        filepath = bpy.data.filepath
        if not filepath:
            self.report({'WARNING'}, "Blend file is not saved")
            return {'CANCELLED'}
            
        filename = bpy.path.basename(filepath).replace(".blend", "")
        root_col = bpy.data.collections.get(filename)
        
        if not root_col:
            self.report({'WARNING'}, f"Root collection '{filename}' not found.")
            return {'CANCELLED'}
            
        visited_objs = set()
        
        def process_col(col):
            prefix = f"{filename}_{col.name}"
            for obj in col.objects:
                if obj.type != 'ARMATURE' and obj not in visited_objs:
                    visited_objs.add(obj)
                    if not obj.name.startswith(prefix):
                        obj.name = f"{prefix}"
            for child in col.children:
                process_col(child)
                
        process_col(root_col)
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ACR_OT_RenameReplaceAsset)

def unregister():
    bpy.utils.unregister_class(ACR_OT_RenameReplaceAsset)