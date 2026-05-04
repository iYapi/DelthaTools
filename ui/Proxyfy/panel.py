import os
import tempfile

class ProxyfyUI:
    def __init__(self, layout, context):
        self.layout = layout
        self.context = context

    def draw(self):
        layout = self.layout
        context = self.context
        s = context.scene.proxyfy_settings

        # 1. Main Run/Revert Buttons
        box = layout.box()
        row = box.row(align=True)
        # row.scale_y = 1.6
        row.operator("proxyfy.run", icon='PLAY')
        row.operator("proxyfy.revert", icon='LOOP_BACK')

        # 2. Boundary Section
        box = layout.box()
        box.label(text="Boundary", icon='MESH_PLANE')
        col = box.column(align=True)
        col.prop(s, "boundary_mode")
        col.prop(s, "weight_threshold", slider=True)

        # 3. Head Meshes Section
        box = layout.box()
        box.label(text="Head Meshes", icon='FACE_MAPS')
        row = box.row()
        row.template_list("UI_UL_list", "head_mesh_names", s, "head_mesh_names", s, "head_mesh_names_index", rows=3)
        col = row.column(align=True)
        col.operator("proxyfy.add_head_mesh", icon='ADD', text="")
        col.operator("proxyfy.remove_head_mesh", icon='REMOVE', text="")
        box.prop(s, "head_decimate_type")
        box.prop(s, "head_decimate_ratio", slider=True)
        
        # 4. Linked Hide Section (The one we enabled multiple select for)
        box = layout.box()
        box.label(text="Linked Hide", icon='HIDE_OFF')
        row = box.row()
        row.template_list("UI_UL_list", "linked_hide_names", s, "linked_hide_names", s, "linked_hide_names_index", rows=3)
        col = row.column(align=True)
        col.operator("proxyfy.add_linked_hide", icon='ADD', text="")
        col.operator("proxyfy.remove_linked_hide", icon='REMOVE', text="")

        # 5. Driver / Property
        box = layout.box()
        box.prop(s, "control_bone_name")

        # 6. Debug
        box = layout.box()
        box.label(text="Debug", icon='CONSOLE')
        box.prop(s, "strict_mode")
        box.prop(s, "log_to_file")
        if s.log_to_file:
            path = os.path.join(tempfile.gettempdir(), "proxyfy_log.txt")
            box.label(text=path, icon='TEXT')