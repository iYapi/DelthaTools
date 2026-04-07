import bpy
import os


class OT_ImportImageSequence(bpy.types.Operator):
    bl_idname = "ivp.import_image_sequence"
    bl_label = "Import Image Sequence"
    bl_description = "Import an image sequence as a plane with the correct settings"
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(
        name="First Frame",
        description="Select any frame of the image sequence (e.g. frame_0001.png)",
        subtype="FILE_PATH",
    )

    # Opens the file browser when called with INVOKE_DEFAULT
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        image_path = bpy.path.abspath(self.filepath)

        if not os.path.isfile(image_path):
            self.report({"ERROR"}, f"File not found: {image_path}")
            return {"CANCELLED"}

        folder = os.path.dirname(image_path)
        file_stem = os.path.splitext(os.path.basename(image_path))[0]
        picked_ext = os.path.splitext(image_path)[1].lower()

        total_frames = sum(
            1
            for f in os.listdir(folder)
            if os.path.splitext(f)[1].lower() == picked_ext
        )

        start_frame = context.scene.frame_current

        offset = 0

        plane_name = file_stem

        bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0))
        plane = context.active_object
        plane.name = plane_name

        mat = bpy.data.materials.new(name=f"{plane_name}_Mat")
        mat.use_nodes = True
        plane.data.materials.append(mat)

        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        tex_coord = nodes.new("ShaderNodeTexCoord")
        tex_coord.location = (-800, 300)

        mapping = nodes.new("ShaderNodeMapping")
        mapping.location = (-600, 300)
        links.new(tex_coord.outputs["UV"], mapping.inputs["Vector"])

        tex_image = nodes.new("ShaderNodeTexImage")
        tex_image.location = (-300, 300)
        links.new(mapping.outputs["Vector"], tex_image.inputs["Vector"])

        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
        bsdf.location = (100, 300)
        links.new(tex_image.outputs["Color"], bsdf.inputs["Base Color"])
        links.new(tex_image.outputs["Alpha"], bsdf.inputs["Alpha"])

        output = nodes.new("ShaderNodeOutputMaterial")
        output.location = (400, 300)
        links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

        mat.blend_method = "BLEND"

        img = bpy.data.images.load(image_path)
        img.source = "SEQUENCE"
        tex_image.image = img

        tex_image.image_user.use_auto_refresh = True
        tex_image.image_user.frame_duration = total_frames
        tex_image.image_user.frame_start = start_frame
        tex_image.image_user.frame_offset = offset

        self.report(
            {"INFO"},
            f"'{plane_name}' — {total_frames} frames, "
            f"start frame {start_frame}, offset {offset}",
        )
        return {"FINISHED"}


def register():
    bpy.utils.register_class(OT_ImportImageSequence)


def unregister():
    bpy.utils.unregister_class(OT_ImportImageSequence)
