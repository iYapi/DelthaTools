import bpy


# ------------------------------------------------------------------------
# Control Camera - Operator
# ------------------------------------------------------------------------
class APB_OT_ViewCamera(bpy.types.Operator):
    """Switch to camera view"""
    bl_idname = "apb.view_camera_operator"
    bl_label = "View Camera"

    def execute(self, context):
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        region_3d = space.region_3d
                        overlay = space.overlay
                        overlay.show_overlays = False
                        region_3d.view_perspective = 'CAMERA'
                        self.report({'INFO'}, "Switched to Camera View")
        return {'FINISHED'}


class APB_OT_return_solid(bpy.types.Operator):
    """Return to previous view"""
    bl_idname = "apb.return_solid"
    bl_label = "Return View"

    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        # space.shading.type = 'MATERIAL'
                        space.shading.type = 'SOLID'
                        space.shading.color_type = 'MATERIAL'
                        break
        return {'FINISHED'}


def register():
    bpy.utils.register_class(APB_OT_ViewCamera)
    bpy.utils.register_class(APB_OT_return_solid)


def unregister():
    bpy.utils.unregister_class(APB_OT_ViewCamera)
    bpy.utils.unregister_class(APB_OT_return_solid)
