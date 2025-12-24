import bpy


# ------------------------------------------------------------------------
# Render Marker Operator
# ------------------------------------------------------------------------
class APB_OT_StartRenderMarker(bpy.types.Operator):
    """Set Render Marker at Current Frame"""
    bl_idname = "apb.start_render_marker"
    bl_label = "Set Render Marker"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        current_frame = scene.frame_current

        markers_to_remove = [m for m in scene.timeline_markers if m.name in {"EX_START"}]

        for marker in markers_to_remove:
            scene.timeline_markers.remove(marker)

        # Add a marker at the current frame
        marker = scene.timeline_markers.new(name="EX_START", frame=current_frame)
        self.report({'INFO'}, f"Render Marker set at frame {current_frame}")
        return {'FINISHED'}


class APB_OT_EndRenderMarker(bpy.types.Operator):
    """Set End Render Marker at Current Frame"""
    bl_idname = "apb.end_render_marker"
    bl_label = "Set End Render Marker"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        current_frame = scene.frame_current

        markers_to_remove = [m for m in scene.timeline_markers if m.name in {"EX_END"}]

        for marker in markers_to_remove:
            scene.timeline_markers.remove(marker)

        # Add a marker at the current frame
        marker = scene.timeline_markers.new(name="EX_END", frame=current_frame)
        self.report({'INFO'}, f"End Render Marker set at frame {current_frame}")
        return {'FINISHED'}


class APB_OT_ClearRenderMarkers(bpy.types.Operator):
    """Clear Render Markers"""
    bl_idname = "apb.clear_render_markers"
    bl_label = "Clear Render Markers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        markers_to_remove = [m for m in scene.timeline_markers if m.name in {"EX_START", "EX_END"}]

        for marker in markers_to_remove:
            scene.timeline_markers.remove(marker)

        self.report({'INFO'}, f"Cleared {len(markers_to_remove)} Render Markers")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(APB_OT_StartRenderMarker)
    bpy.utils.register_class(APB_OT_EndRenderMarker)
    bpy.utils.register_class(APB_OT_ClearRenderMarkers)


def unregister():
    bpy.utils.unregister_class(APB_OT_StartRenderMarker)
    bpy.utils.unregister_class(APB_OT_EndRenderMarker)
    bpy.utils.unregister_class(APB_OT_ClearRenderMarkers)
