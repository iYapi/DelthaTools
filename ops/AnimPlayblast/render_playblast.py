import bpy


class APB_OT_Render(bpy.types.Operator):
    bl_idname = "apb.render_playblast"
    bl_label = "Render Playblast"
    bl_description = "Render Animation Playblast"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.apb.apply_preset()

        camera = bpy.context.scene.camera
        if camera:
            camera.select_set(True)
            bpy.context.view_layer.objects.active = camera
            bpy.ops.render.opengl(animation=True)
        else:
            print("No camera found in the scene.")
            self.report({'ERROR'}, "No camera found in the scene.")
            return {'CANCELLED'}

        self.report({'INFO'}, "Rendering started")

        bpy.ops.apb.return_solid()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(APB_OT_Render)


def unregister():
    bpy.utils.unregister_class(APB_OT_Render)
