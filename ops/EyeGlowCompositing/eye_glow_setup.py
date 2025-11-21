import bpy
import os
from ...utils.file_manager import FileManager


class OT_EyeGlowSetup(bpy.types.Operator):
    bl_idname = "egc.append_blend"
    bl_label = "Append compositing node Setup"
    bl_description = "Append compositing node setup from presets blend file"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        s = context.scene
        props = s.lighting_setup
        raw_path = props.filepath
        properties_props = s.lighting_props
        filepath = FileManager.get_filepath(raw_path)
        if not filepath:
            self.report({'ERROR'}, "No presets file path specified")
            return {'CANCELLED'}

        node_group_name = "Eye_Glow_Setup"

        scene = bpy.context.scene
        scene.use_nodes = True
        scene.render.use_compositing = True
        tree = scene.node_tree

        # Append node group if not found
        node_group = bpy.data.node_groups.get(node_group_name)

        if node_group is None:
            node_tree_dir = os.path.join(filepath, "NodeTree")
            node_tree_filepath = os.path.join(node_tree_dir, node_group_name)

            bpy.ops.wm.append(
                filepath=node_tree_filepath,
                directory=node_tree_dir,
                filename=node_group_name
            )

            node_group = bpy.data.node_groups.get(node_group_name)

            if node_group is None:
                self.report({'ERROR'}, f"Failed to append node group '{node_group_name}' from file:\n{filepath}")

        # Create node Group di compositor
        group_node = tree.nodes.new("CompositorNodeGroup")
        group_node.node_tree = node_group
        group_node.name = "Eye_Glow_Setup"
        group_node.label = "Eye_Glow_Setup"
        group_node.location = (200, 0)

        # Create node Cryptomatte V2 in compositor
        crypto_node = tree.nodes.new("CompositorNodeCryptomatteV2")
        crypto_node.name = "Cryptomatte_Eye_Glow"
        crypto_node.label = "Cryptomatte_Eye_Glow"
        crypto_node.layer_name = "Comp.CryptoMaterial"
        crypto_node.matte_id = (
            "eyes,eyes.001,eyes.002,eyes.003,eyes.004,eyes.005,eyes.006,eyes.007,"
            "eyes.008,eyes.009,eyes.010,eyes.011,eyes.012,eyes.013,eyes.014,eyes.015,"
            "eyes.016,eyes.017,eyes.018,eyes.019,eyes.020,eyes.021,eyes.022,eyes.023,"
            "eyes.024,eyes.025,eyes.026,eyes.027,eyes.028,eyes.029,eyes.030"
        )
        crypto_node.location = (-200, 0)

        # Connect Cryptomatte output[0] -> Eye_Glow_Setup input[1]
        links = tree.links

        if crypto_node.outputs and len(group_node.inputs) > 1:
            links.new(crypto_node.outputs[0], group_node.inputs[1])
        else:
            self.report({'ERROR'}, "Socket cryptomatte output[0] or Eye_Glow_Setup input[1] not found.")

        self.report({'INFO'}, "Eye Glow compositing setup appended successfully.")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OT_EyeGlowSetup)


def unregister():
    bpy.utils.unregister_class(OT_EyeGlowSetup)
