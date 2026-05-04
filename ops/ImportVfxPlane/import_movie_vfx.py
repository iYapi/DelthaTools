import bpy
import os


def get_movie_total_frames(movie_path: str) -> int:
    try:
        clip = bpy.data.movieclips.load(movie_path)
        total = clip.frame_duration
        bpy.data.movieclips.remove(clip)
        print(f"[get_movie_total_frames] bpy → {total} frames")
        return total
    except Exception as e:
        print(f"[get_movie_total_frames] bpy failed: {e}")

    return 0


class OT_ImportMovieTexture(bpy.types.Operator):
    bl_idname = "ivp.import_movie_texture"
    bl_label = "Import Movie Texture"
    bl_description = (
        "Pick a movie file (.mov, .mp4, .avi). "
        "Total frames, start frame, and plane name are resolved automatically."
    )
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(
        name="Movie File",
        description="Select a movie file (e.g. clip.mov)",
        subtype="FILE_PATH",
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        movie_path = bpy.path.abspath(self.filepath)

        if not os.path.isfile(movie_path):
            self.report({"ERROR"}, f"File not found: {movie_path}")
            return {"CANCELLED"}

        file_stem = os.path.splitext(os.path.basename(movie_path))[0]

        total_frames = get_movie_total_frames(movie_path)
        start_frame = context.scene.frame_current
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

        output = nodes.new("ShaderNodeOutputMaterial")
        output.location = (400, 300)
        links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

        mat.blend_method = "BLEND"

        img = bpy.data.images.load(movie_path)
        img.source = "MOVIE"
        tex_image.image = img

        tex_image.image_user.use_auto_refresh = True
        tex_image.image_user.frame_duration = (
            total_frames if total_frames > 0 else 1048574
        )
        tex_image.image_user.frame_start = start_frame

        self.report(
            {"INFO"},
            f"[Movie] '{plane_name}' — {total_frames} frames detected, "
            f"start frame {start_frame}",
        )
        return {"FINISHED"}


def register():
    bpy.utils.register_class(OT_ImportMovieTexture)


def unregister():
    bpy.utils.unregister_class(OT_ImportMovieTexture)
