import bpy
import bmesh
import os
import tempfile
import traceback
from mathutils import Matrix
from bpy.types import Operator, Panel

# ---------------------------------------------------------------------------
# List management operators (head mesh names)
# ---------------------------------------------------------------------------

class PROXYFY_OT_add_head_mesh(Operator):
    bl_idname = "proxyfy.add_head_mesh"
    bl_label = "Add Head Meshes"
    bl_description = "Add all selected mesh objects to the Head Mesh list"

    def execute(self, context):
        s = context.scene.proxyfy_settings
        selected_objs = context.selected_objects
        
        if not selected_objs:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}

        # Get existing names to prevent duplicates
        existing_names = {item.name for item in s.head_mesh_names}
        added_count = 0

        for obj in selected_objs:
            # Check if it's a mesh and not already in our list
            if obj.type == 'MESH':
                if obj.name not in existing_names:
                    item = s.head_mesh_names.add()
                    item.name = obj.name
                    added_count += 1
                else:
                    self.report({'INFO'}, f"'{obj.name}' is already in the list")
            else:
                self.report({'INFO'}, f"Skipped '{obj.name}' (not a mesh)")

        if added_count > 0:
            self.report({'INFO'}, f"Added {added_count} mesh(es) to the list")
        
        return {'FINISHED'}


class PROXYFY_OT_remove_head_mesh(Operator):
    bl_idname = "proxyfy.remove_head_mesh"
    bl_label = "Remove Head Mesh"

    def execute(self, context):
        s = context.scene.proxyfy_settings
        idx = s.head_mesh_names_index
        if 0 <= idx < len(s.head_mesh_names):
            s.head_mesh_names.remove(idx)
            s.head_mesh_names_index = max(0, idx - 1)
        return {'FINISHED'}


class PROXYFY_OT_add_linked_hide(Operator):
    bl_idname = "proxyfy.add_linked_hide"
    bl_label = "Add Linked-Hide Objects"
    bl_description = "Add all selected objects to Linked-Hide list"

    def execute(self, context):
        s = context.scene.proxyfy_settings
        # Get all selected objects
        selected_objs = context.selected_objects
        
        if not selected_objs:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}

        # Create a set of existing names to avoid duplicates if desired
        existing_names = {item.name for item in s.linked_hide_names}

        for obj in selected_objs:
            if obj.name not in existing_names:
                item = s.linked_hide_names.add()
                item.name = obj.name
            else:
                self.report({'INFO'}, f"Object '{obj.name}' is already in the list")

        return {'FINISHED'}

class PROXYFY_OT_remove_linked_hide(Operator):
    bl_idname = "proxyfy.remove_linked_hide"
    bl_label = "Remove Linked-Hide Object"

    def execute(self, context):
        s = context.scene.proxyfy_settings
        idx = s.linked_hide_names_index
        if 0 <= idx < len(s.linked_hide_names):
            s.linked_hide_names.remove(idx)
            s.linked_hide_names_index = max(0, idx - 1)
        return {'FINISHED'}


# ---------------------------------------------------------------------------
# Core logic  (extracted from original script, now wrapped in a class)
# ---------------------------------------------------------------------------

class _ProxyfyCore:
    """All logic from proxyfy_mk11.py, ported to use self.s (settings) and
    self.ctx instead of module-level constants."""

    PROXY_TAG_KEY        = "__is_proxyfy_chunk__"
    PROXY_SOURCE_KEY     = "__proxyfy_source__"
    PROXY_HEAD_TAG_KEY   = "__is_proxyfy_head__"
    PROXY_LINKED_TAG_KEY = "__is_proxyfy_linked_hide__"
    LEGACY_BONE_NAMES    = ("c-pos",)
    LEGACY_PROP_NAMES    = ("proxyfy on/off", "proxyfy_toggle")
    HEAD_DECIMATE_NAME   = "decimate_facial"

    def __init__(self, context, settings, report_fn):
        self.ctx = context
        self.s = settings
        self.report = report_fn
        self._log_lines = []
        self._counts = {"ok": 0, "warn": 0, "err": 0}

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    def _log(self, msg):
        print(msg)
        self._log_lines.append(msg)

    def _ok(self, msg):
        self._counts["ok"] += 1
        self._log(f"[OK]   {msg}")

    def _warn(self, msg):
        self._counts["warn"] += 1
        self._log(f"[WARN] {msg}")

    def _err(self, msg):
        self._counts["err"] += 1
        self._log(f"[ERR]  {msg}")

    def _banner(self, text, char="=", width=72):
        self._log("")
        self._log(char * width)
        self._log(f" {text} ".center(width, char))
        self._log(char * width)

    def _fail(self, phase, reason, hint=None):
        self._banner(f"FAILED at {phase}", char="!", width=72)
        self._log(f"!! REASON: {reason}")
        if hint:
            self._log(f"!! HINT  : {hint}")
        self._log("!" * 72)
        if self.s.strict_mode:
            raise RuntimeError(f"[{phase}] {reason}")

    def flush_log(self):
        if not self.s.log_to_file:
            return
        path = os.path.join(tempfile.gettempdir(), "proxyfy_log.txt")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(self._log_lines))
            print(f"[PROXYFY] Log written: {path}")
        except Exception as e:
            print(f"[PROXYFY] Log write failed: {e}")

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------
    def _ensure_object_mode(self):
        try:
            if self.ctx.object and self.ctx.object.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
        except Exception:
            pass

    def _set_active(self, obj):
        self._ensure_object_mode()
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        self.ctx.view_layer.objects.active = obj

    def _safe_remove_object(self, obj):
        mesh = obj.data if obj.type == 'MESH' else None
        for coll in list(obj.users_collection):
            coll.objects.unlink(obj)
        try:
            bpy.data.objects.remove(obj, do_unlink=True)
        except Exception:
            pass
        if mesh is not None and mesh.users == 0:
            try:
                bpy.data.meshes.remove(mesh)
            except Exception:
                pass

    def _get_character_root_collection(self, obj):
        scene_root = self.ctx.scene.collection
        if not obj.users_collection:
            return scene_root
        start_coll = obj.users_collection[0]

        def find_parent(target, parent):
            for child in parent.children:
                if child == target:
                    return parent
                found = find_parent(target, child)
                if found is not None:
                    return found
            return None

        current = start_coll
        for _ in range(64):
            parent = find_parent(current, scene_root)
            if parent is None or parent == scene_root:
                break
            current = parent
        return current

    def _get_or_create_collection_for_root(self, root_coll, name):
        scene_root = self.ctx.scene.collection
        coll = root_coll.children.get(name)
        if coll is None:
            coll = bpy.data.collections.get(name)
            if coll is None:
                coll = bpy.data.collections.new(name)
            if root_coll.children.get(coll.name) is None:
                root_coll.children.link(coll)
        if root_coll != scene_root and scene_root.children.get(coll.name) is not None:
            scene_root.children.unlink(coll)
        return coll

    def _ensure_obj_in_collection(self, obj, coll):
        if coll.name not in [c.name for c in obj.users_collection]:
            coll.objects.link(obj)

    def _add_childof_keep_world(self, child_obj, armature_obj, bone_name):
        if bone_name is not None and armature_obj.pose.bones.get(bone_name) is None:
            self._warn(f"Bone '{bone_name}' tidak ada di {armature_obj.name}.")
            return False
        con = child_obj.constraints.new('CHILD_OF')
        con.name = f"CHILD_OF_{bone_name or 'ROOT'}"
        con.target = armature_obj
        if bone_name:
            con.subtarget = bone_name
        con.use_location_x = con.use_location_y = con.use_location_z = True
        con.use_rotation_x = con.use_rotation_y = con.use_rotation_z = True
        con.use_scale_x = con.use_scale_y = con.use_scale_z = True
        con.influence = 1.0
        try:
            if bone_name:
                bone_world = (armature_obj.matrix_world
                              @ armature_obj.pose.bones[bone_name].matrix)
            else:
                bone_world = armature_obj.matrix_world.copy()
            con.inverse_matrix = bone_world.inverted() @ child_obj.matrix_world.copy()
            return True
        except Exception as e:
            try:
                self._set_active(child_obj)
                bpy.ops.object.constraint_set_active(constraint=con.name)
                bpy.ops.constraint.childof_set_inverse(
                    constraint=con.name, owner='OBJECT')
                return True
            except Exception as e2:
                self._err(f"Child Of inverse gagal '{child_obj.name}': {e} / {e2}")
                con.mute = True
                return False

    def _parent_to_bone_keep_world(self, child_obj, armature_obj, bone_name):
        pb = armature_obj.pose.bones.get(bone_name) if bone_name else None
        child_world = child_obj.matrix_world.copy()
        child_obj.parent = armature_obj
        if pb:
            child_obj.parent_type = 'BONE'
            child_obj.parent_bone = bone_name
            bone_world = armature_obj.matrix_world @ pb.matrix
        else:
            child_obj.parent_type = 'OBJECT'
            bone_world = armature_obj.matrix_world.copy()
        child_obj.matrix_parent_inverse = bone_world.inverted() @ child_world
        return True

    def _link_to_bone(self, child_obj, armature_obj, bone_name):
        if self.s.use_child_of_constraint:
            if self._add_childof_keep_world(child_obj, armature_obj, bone_name):
                return True
            return self._parent_to_bone_keep_world(child_obj, armature_obj, bone_name)
        return self._parent_to_bone_keep_world(child_obj, armature_obj, bone_name)

    # ------------------------------------------------------------------
    # Phase 1: Preflight
    # ------------------------------------------------------------------
    def phase1_preflight(self):
        self._banner("PHASE 1/7 : PREFLIGHT CHECK")
        s = self.s

        if s.boundary_mode not in ('OVERLAP', 'MAJORITY', 'SHRINK'):
            self._fail("PHASE 1 / CONFIG",
                       f"BOUNDARY_MODE '{s.boundary_mode}' invalid.")
        if s.head_decimate_type not in ('COLLAPSE', 'UNSUBDIV', 'DISSOLVE'):
            self._fail("PHASE 1 / CONFIG",
                       f"HEAD_DECIMATE_TYPE '{s.head_decimate_type}' invalid.")

        selected_meshes = [o for o in self.ctx.selected_objects if o.type == 'MESH']
        if not selected_meshes:
            self._fail("PHASE 1 / MESH SELECTION",
                       "Tidak ada objek MESH terseleksi.",
                       hint="Pilih minimal satu mesh.")

        head_name_set = {item.name for item in s.head_mesh_names}
        head_meshes = []
        for item in s.head_mesh_names:
            obj = bpy.data.objects.get(item.name)
            if obj is None:
                self._warn(f"HEAD_MESH_NAMES: '{item.name}' tidak ada di scene.")
                continue
            if obj.type != 'MESH':
                self._warn(f"HEAD_MESH_NAMES: '{item.name}' bukan MESH.")
                continue
            head_meshes.append(obj)

        linked_hide_objs = []
        for item in s.linked_hide_names:
            obj = bpy.data.objects.get(item.name)
            if obj is None:
                self._warn(f"LINKED_HIDE_NAMES: '{item.name}' tidak ada di scene.")
                continue
            linked_hide_objs.append(obj)

        # Resolve control armature
        mesh_arm_map = {}
        for m in selected_meshes:
            arm_mod = next((mod for mod in m.modifiers
                            if mod.type == 'ARMATURE'
                            and getattr(mod, "object", None)
                            and mod.object.type == 'ARMATURE'), None)
            if arm_mod:
                mesh_arm_map[m.name] = arm_mod.object

        armature_candidates = []
        for o in self.ctx.selected_objects:
            if o.type == 'ARMATURE':
                armature_candidates.append(("selected", o))
        for mname, arm in mesh_arm_map.items():
            if not any(a is arm for _, a in armature_candidates):
                armature_candidates.append((f"modifier:{mname}", arm))

        if not armature_candidates:
            self._fail("PHASE 1 / ARMATURE RESOLVE",
                       "Tidak ada armature terseleksi & tidak ada di modifier.")

        control_arm = None
        actual_bone_name = None
        for source, arm in armature_candidates:
            if arm.pose is None:
                continue
            if s.control_bone_name in arm.pose.bones:
                control_arm = arm
                actual_bone_name = s.control_bone_name
                break
            for legacy in self.LEGACY_BONE_NAMES:
                if legacy in arm.pose.bones:
                    control_arm = arm
                    actual_bone_name = legacy
                    self._warn(f"Legacy bone '{legacy}' dipakai di {arm.name}.")
                    break
            if control_arm:
                break

        if control_arm is None:
            self._fail("PHASE 1 / CONTROL BONE",
                       f"Tidak ada armature yang punya bone '{s.control_bone_name}'.",
                       hint="Rename bone atau ubah Control Bone Name di panel.")

        if control_arm.library is not None:
            self._fail("PHASE 1 / CONTROL ARMATURE STATE",
                       f"Armature '{control_arm.name}' LINKED.",
                       hint="Make Local atau Library Override dulu.")

        split_meshes = [m for m in selected_meshes
                        if m.name not in head_name_set]
        self._ok(f"Preflight OK. arm='{control_arm.name}', bone='{actual_bone_name}'")
        return split_meshes, head_meshes, linked_hide_objs, control_arm, actual_bone_name

    # ------------------------------------------------------------------
    # Phase 2: Validate heads
    # ------------------------------------------------------------------
    def phase2_validate_heads(self, head_meshes):
        self._banner("PHASE 2/7 : VALIDATE HEAD MESHES")
        if not head_meshes:
            return
        problems = []
        for hm in head_meshes:
            if hm.data.shape_keys and len(hm.data.shape_keys.key_blocks) > 0:
                sk_names = [kb.name for kb in hm.data.shape_keys.key_blocks][:5]
                problems.append((hm.name, len(hm.data.shape_keys.key_blocks), sk_names))
        if problems:
            details = "; ".join(f"{n}({c} keys)" for n, c, _ in problems)
            self._fail("PHASE 2 / HEAD SHAPE KEYS",
                       f"Head meshes punya shape keys: {details}. "
                       f"Hapus shape keys sebelum menjalankan Proxyfy.",
                       hint="Properties > Object Data > Shape Keys > X")
        self._ok(f"Validasi {len(head_meshes)} head mesh: tidak ada shape keys.")

    # ------------------------------------------------------------------
    # Phase 3: Custom property
    # ------------------------------------------------------------------
    def phase3_create_property(self, arm_obj, actual_bone):
        self._banner("PHASE 3/7 : CREATE CUSTOM PROPERTY")
        s = self.s
        pb = arm_obj.pose.bones.get(actual_bone)
        if pb is None:
            self._fail("PHASE 3 / BONE LOOKUP", f"Bone '{actual_bone}' hilang.")

        # Migrate legacy
        initial_val = None
        if s.prop_name in pb:
            try:
                initial_val = int(pb[s.prop_name])
            except Exception:
                pass
        if initial_val is None:
            for legacy in self.LEGACY_PROP_NAMES:
                if legacy in pb:
                    try:
                        initial_val = int(pb[legacy])
                    except Exception:
                        pass
                    try:
                        del pb[legacy]
                    except Exception:
                        pass

        final_val = s.prop_default_value if initial_val is None else initial_val
        try:
            pb[s.prop_name] = final_val
        except Exception as e:
            self._fail("PHASE 3 / SET PROPERTY", f"Assign gagal: {e}")

        if s.prop_name not in pb:
            self._fail("PHASE 3 / VERIFY",
                       f"'{s.prop_name}' tidak ada di bone setelah assign.")

        data_path_rel = f'pose.bones["{actual_bone}"]["{s.prop_name}"]'
        try:
            arm_obj.path_resolve(data_path_rel)
        except Exception as e:
            self._fail("PHASE 3 / PATH RESOLVE", f"path_resolve gagal: {e}")

        try:
            ui = pb.id_properties_ui(s.prop_name)
            ui.update(min=0, max=1, soft_min=0, soft_max=1,
                      description=s.prop_description)
        except Exception as e:
            self._warn(f"id_properties_ui.update gagal: {e}")

        try:
            arm_obj.property_overridable_library_set(data_path_rel, True)
        except Exception as e:
            self._warn(f"overridable_library_set gagal: {e}")

        try:
            arm_obj.update_tag()
            for area in self.ctx.screen.areas:
                area.tag_redraw()
        except Exception:
            pass

        self._ok(f"Property '{s.prop_name}' = {final_val} set on {arm_obj.name}.{actual_bone}")

    # ------------------------------------------------------------------
    # Driver helpers
    # ------------------------------------------------------------------
    def _add_hide_driver_verified(self, obj, arm_obj, bone_name,
                                  data_path_attr, expression, tag):
        s = self.s
        if obj.animation_data is None:
            obj.animation_data_create()

        fcurve = next((fc for fc in obj.animation_data.drivers
                       if fc.data_path == data_path_attr), None)
        if fcurve is None:
            try:
                fcurve = obj.driver_add(data_path_attr)
            except Exception as e:
                self._fail(f"{tag} / DRIVER_ADD",
                           f"driver_add('{data_path_attr}') di {obj.name} gagal: {e}")

        drv = fcurve.driver
        drv.type = 'SCRIPTED'
        drv.expression = expression
        while drv.variables:
            drv.variables.remove(drv.variables[0])
        var = drv.variables.new()
        var.name = "var"
        var.type = 'SINGLE_PROP'
        t = var.targets[0]
        t.id_type = 'OBJECT'
        t.id = arm_obj
        t.data_path = f'pose.bones["{bone_name}"]["{s.prop_name}"]'

        try:
            arm_obj.path_resolve(t.data_path)
        except Exception as e:
            self._fail(f"{tag} / DRIVER_VERIFY",
                       f"Target path tidak resolve: {e}")

    def _attach_visibility_drivers(self, obj, arm_obj, bone_name, mode, tag):
        expr = "var" if mode == "SOURCE" else "1 - var"
        self._add_hide_driver_verified(
            obj, arm_obj, bone_name, "hide_viewport", expr, tag)
        self._add_hide_driver_verified(
            obj, arm_obj, bone_name, "hide_render", expr, tag)

    # ------------------------------------------------------------------
    # Phase 4: Drivers on source & linked-hide
    # ------------------------------------------------------------------
    def phase4_driver_source(self, split_meshes, head_meshes, linked_hide_objs,
                             control_arm, actual_bone):
        self._banner("PHASE 4/7 : ATTACH DRIVERS TO SOURCE & LINKED-HIDE")
        if not self.s.drive_source_visibility:
            return
        for src in split_meshes:
            self._attach_visibility_drivers(
                src, control_arm, actual_bone, "SOURCE",
                tag=f"PHASE 4 / source / {src.name}")
        for hm in head_meshes:
            self._attach_visibility_drivers(
                hm, control_arm, actual_bone, "SOURCE",
                tag=f"PHASE 4 / head_source / {hm.name}")
        for lh in linked_hide_objs:
            self._attach_visibility_drivers(
                lh, control_arm, actual_bone, "SOURCE",
                tag=f"PHASE 4 / linked_hide / {lh.name}")
            lh[self.PROXY_LINKED_TAG_KEY] = True
        self._ok(f"Drivers dipasang: {len(split_meshes)} split + "
                 f"{len(head_meshes)} head + {len(linked_hide_objs)} linked-hide.")

    # ------------------------------------------------------------------
    # Ownership helpers
    # ------------------------------------------------------------------
    def _build_vertex_weights(self, mesh, relevant_vg_idx):
        threshold = self.s.weight_threshold
        vw = [dict() for _ in mesh.vertices]
        for v in mesh.vertices:
            for g in v.groups:
                if g.group in relevant_vg_idx and g.weight > threshold:
                    vw[v.index][g.group] = g.weight
        return vw

    def _build_face_ownership_majority(self, mesh, vert_weights):
        face_owner = [-1] * len(mesh.polygons)
        for poly in mesh.polygons:
            agg = {}
            for vi in poly.vertices:
                for vg_idx, w in vert_weights[vi].items():
                    agg[vg_idx] = agg.get(vg_idx, 0.0) + w
            if agg:
                face_owner[poly.index] = max(agg.items(), key=lambda t: t[1])[0]
        return face_owner

    def _build_face_ownership_overlap(self, mesh, vert_weights):
        face_owners = [frozenset()] * len(mesh.polygons)
        for poly in mesh.polygons:
            owners = set()
            for vi in poly.vertices:
                owners.update(vert_weights[vi].keys())
            face_owners[poly.index] = frozenset(owners)
        return face_owners

    def _build_vert_ownership_shrink(self, mesh, vert_weights):
        owner = [-1] * len(mesh.vertices)
        for vi, wmap in enumerate(vert_weights):
            if wmap:
                owner[vi] = max(wmap.items(), key=lambda t: t[1])[0]
        return owner

    # ------------------------------------------------------------------
    # Chunk extraction
    # ------------------------------------------------------------------
    def _clean_loose(self, bm):
        if not self.s.clean_loose_geometry:
            return
        loose_edges = [e for e in bm.edges if not e.link_faces]
        if loose_edges:
            bmesh.ops.delete(bm, geom=loose_edges, context='EDGES')
        loose_verts = [v for v in bm.verts if not v.link_edges]
        if loose_verts:
            bmesh.ops.delete(bm, geom=loose_verts, context='VERTS')

    def _finalize_new_obj(self, new_mesh, src, new_name, proxy_coll):
        s = self.s
        new_mesh.update()
        new_obj = bpy.data.objects.new(new_name, new_mesh)
        new_obj.matrix_world = src.matrix_world.copy()
        self._ensure_obj_in_collection(new_obj, proxy_coll)

        if s.strip_shape_keys and new_obj.data.shape_keys is not None:
            self._set_active(new_obj)
            try:
                while new_obj.data.shape_keys and new_obj.data.shape_keys.key_blocks:
                    bpy.ops.object.shape_key_remove(all=True)
                    break
            except Exception:
                pass

        if s.decimate_ratio < 1.0 and len(new_obj.data.polygons) > 0:
            self._set_active(new_obj)
            mod = new_obj.modifiers.new(name="Decimate_LOD", type='DECIMATE')
            mod.ratio = max(0.01, s.decimate_ratio)
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
            except Exception as e:
                self._warn(f"Decimate apply gagal di {new_obj.name}: {e}")

        new_obj[self.PROXY_TAG_KEY] = True
        new_obj[self.PROXY_SOURCE_KEY] = src.name
        return new_obj

    def _extract_chunk(self, src, ownership_data, target_vg_idx,
                       is_unassigned, new_name, proxy_coll):
        mode = self.s.boundary_mode
        new_mesh = src.data.copy()
        new_mesh.name = new_name
        bm = bmesh.new()
        bm.from_mesh(new_mesh)

        if mode == 'SHRINK':
            bm.verts.ensure_lookup_table()
            keep_v = ((lambda vi: ownership_data[vi] == -1) if is_unassigned
                      else (lambda vi: ownership_data[vi] == target_vg_idx))
            del_verts = [v for v in bm.verts if not keep_v(v.index)]
            if del_verts:
                bmesh.ops.delete(bm, geom=del_verts, context='VERTS')
        else:
            bm.faces.ensure_lookup_table()
            if mode == 'MAJORITY':
                keep_f = ((lambda fi: ownership_data[fi] == -1) if is_unassigned
                          else (lambda fi: ownership_data[fi] == target_vg_idx))
            else:  # OVERLAP
                keep_f = ((lambda fi: len(ownership_data[fi]) == 0) if is_unassigned
                          else (lambda fi: target_vg_idx in ownership_data[fi]))
            del_faces = [f for f in bm.faces if not keep_f(f.index)]
            if del_faces:
                bmesh.ops.delete(bm, geom=del_faces, context='FACES')

        self._clean_loose(bm)

        if len(bm.faces) == 0 and len(bm.verts) == 0:
            bm.free()
            try:
                bpy.data.meshes.remove(new_mesh)
            except Exception:
                pass
            return None

        bm.to_mesh(new_mesh)
        bm.free()
        return self._finalize_new_obj(new_mesh, src, new_name, proxy_coll)

    def _clear_previous_chunks(self, src, proxy_coll):
        if proxy_coll is None:
            return
        for obj in list(proxy_coll.objects):
            if (obj.get(self.PROXY_TAG_KEY)
                    and obj.get(self.PROXY_SOURCE_KEY) == src.name):
                self._safe_remove_object(obj)

    def _clear_previous_head(self, src_name, proxy_coll):
        if proxy_coll is None:
            return
        for obj in list(proxy_coll.objects):
            if (obj.get(self.PROXY_HEAD_TAG_KEY)
                    and obj.get(self.PROXY_SOURCE_KEY) == src_name):
                self._safe_remove_object(obj)

    # ------------------------------------------------------------------
    # Phase 5: Split chunks
    # ------------------------------------------------------------------
    def phase5_chunks_and_proxy_drivers(self, split_meshes, control_arm, actual_bone):
        self._banner("PHASE 5/7 : GENERATE PROXY CHUNKS (SPLIT)")
        s = self.s
        all_proxy = []
        processed_colls = set()

        for src in split_meshes:
            arm_mod = next((m for m in src.modifiers
                            if m.type == 'ARMATURE'
                            and getattr(m, "object", None)
                            and m.object.type == 'ARMATURE'), None)
            if not arm_mod:
                self._warn(f"{src.name}: tanpa Armature modifier. Dilewati.")
                continue
            arm_obj_for_parent = arm_mod.object

            char_root = self._get_character_root_collection(src)
            proxy_coll = self._get_or_create_collection_for_root(char_root, "proxy_mesh")
            processed_colls.add(proxy_coll)

            if s.clean_previous_run:
                self._clear_previous_chunks(src, proxy_coll)

            if s.apply_mirror_first:
                self._set_active(src)
                for m in [mm for mm in src.modifiers if mm.type == 'MIRROR']:
                    try:
                        bpy.ops.object.modifier_apply(modifier=m.name)
                    except Exception as e:
                        self._warn(f"{src.name}: gagal apply Mirror '{m.name}': {e}")

            vg_all = list(src.vertex_groups)
            if s.only_groups_with_matching_bone:
                vg_list = [vg for vg in vg_all
                           if vg.name in arm_obj_for_parent.data.bones]
            else:
                vg_list = vg_all[:]

            if not vg_list and not s.make_unassigned_chunk:
                self._warn(f"{src.name}: tidak ada VG relevan. Dilewati.")
                continue

            relevant_vg_idx = {vg.index for vg in vg_list}
            vert_weights = self._build_vertex_weights(src.data, relevant_vg_idx)

            if s.boundary_mode == 'MAJORITY':
                ownership_data = self._build_face_ownership_majority(
                    src.data, vert_weights)
                has_unassigned = any(o == -1 for o in ownership_data)
            elif s.boundary_mode == 'OVERLAP':
                ownership_data = self._build_face_ownership_overlap(
                    src.data, vert_weights)
                has_unassigned = any(len(o) == 0 for o in ownership_data)
            else:
                ownership_data = self._build_vert_ownership_shrink(
                    src.data, vert_weights)
                has_unassigned = any(o == -1 for o in ownership_data)

            created = []
            for vg in vg_list:
                chunk_name = (f"{src.name}__{vg.name}" if s.use_prefix_srcname
                              else vg.name)
                piece = self._extract_chunk(
                    src, ownership_data, vg.index, False, chunk_name, proxy_coll)
                if piece is None:
                    continue
                if not self._link_to_bone(piece, arm_obj_for_parent, vg.name):
                    self._warn(f"{src.name}: link bone '{vg.name}' gagal.")
                created.append(piece)

            if s.make_unassigned_chunk and has_unassigned:
                uname = (f"{src.name}__{s.unassigned_name}"
                         if s.use_prefix_srcname else s.unassigned_name)
                piece = self._extract_chunk(
                    src, ownership_data, -1, True, uname, proxy_coll)
                if piece is not None:
                    self._link_to_bone(piece, arm_obj_for_parent, bone_name=None)
                    created.append(piece)

            if s.join_per_source and len(created) > 1:
                self._set_active(created[0])
                for c in created[1:]:
                    c.select_set(True)
                try:
                    bpy.ops.object.join()
                    joined = self.ctx.view_layer.objects.active
                    joined.name = f"{src.name}__proxy"
                    created = [joined]
                except Exception as e:
                    self._warn(f"Join gagal: {e}")

            for piece in created:
                self._attach_visibility_drivers(
                    piece, control_arm, actual_bone, "PROXY",
                    tag=f"PHASE 5 / {piece.name}")

            all_proxy.extend(created)
            self._ok(f"{src.name}: {len(created)} chunk dibuat.")

        return all_proxy, processed_colls

    # ------------------------------------------------------------------
    # Phase 6: Head mesh proxies
    # ------------------------------------------------------------------
    def _make_head_proxy(self, head_obj, proxy_coll, control_arm, actual_bone):
        s = self.s
        self._clear_previous_head(head_obj.name, proxy_coll)

        self._set_active(head_obj)
        try:
            bpy.ops.object.duplicate(linked=False)
        except Exception as e:
            self._err(f"{head_obj.name}: duplicate gagal: {e}")
            return None

        new_obj = self.ctx.view_layer.objects.active
        if new_obj is None or new_obj is head_obj:
            self._err(f"{head_obj.name}: duplicate tidak menghasilkan object baru.")
            return None

        proxy_name = f"{head_obj.name}__head_proxy"
        new_obj.name = proxy_name
        new_obj.data.name = proxy_name

        for coll in list(new_obj.users_collection):
            coll.objects.unlink(new_obj)
        self._ensure_obj_in_collection(new_obj, proxy_coll)

        if s.head_apply_subsurf_first:
            self._set_active(new_obj)
            for mname in [mm.name for mm in new_obj.modifiers if mm.type == 'SUBSURF']:
                try:
                    bpy.ops.object.modifier_apply(modifier=mname)
                except Exception as e:
                    self._err(f"{new_obj.name}: Apply Subsurf '{mname}' gagal: {e}")
                    self._safe_remove_object(new_obj)
                    return None

        self._set_active(new_obj)
        dec = new_obj.modifiers.new(name=self.HEAD_DECIMATE_NAME, type='DECIMATE')
        dec.decimate_type = s.head_decimate_type
        if s.head_decimate_type == 'COLLAPSE':
            dec.ratio = s.head_decimate_ratio
            dec.use_symmetry = s.head_decimate_use_symmetry
            try:
                dec.symmetry_axis = s.head_decimate_symmetry_axis
            except Exception:
                pass
            dec.use_collapse_triangulate = s.head_decimate_triangulate

        try:
            bpy.ops.object.modifier_apply(modifier=dec.name)
        except Exception as e:
            self._err(f"{new_obj.name}: APPLY DECIMATE GAGAL: {e}")
            self._safe_remove_object(new_obj)
            return None

        new_obj[self.PROXY_TAG_KEY] = True
        new_obj[self.PROXY_HEAD_TAG_KEY] = True
        new_obj[self.PROXY_SOURCE_KEY] = head_obj.name
        self._attach_visibility_drivers(
            new_obj, control_arm, actual_bone, "PROXY",
            tag=f"PHASE 6 / {new_obj.name}")

        has_arm = any(m.type == 'ARMATURE' for m in new_obj.modifiers)
        if not has_arm:
            self._warn(f"{new_obj.name}: tidak ada Armature modifier. "
                       f"Facial acting tidak akan jalan.")
        self._ok(f"Head proxy: {new_obj.name} "
                 f"(poly={len(new_obj.data.polygons)}, "
                 f"arm_mod={'YES' if has_arm else 'NO'})")
        return new_obj

    def phase6_head_meshes(self, head_meshes, control_arm, actual_bone):
        self._banner("PHASE 6/7 : HEAD MESH PROXIES (DECIMATE)")
        if not head_meshes:
            return [], set()

        head_proxies = []
        processed_colls = set()
        for head_obj in head_meshes:
            char_root = self._get_character_root_collection(head_obj)
            proxy_coll = self._get_or_create_collection_for_root(
                char_root, "proxy_mesh")
            processed_colls.add(proxy_coll)
            result = self._make_head_proxy(
                head_obj, proxy_coll, control_arm, actual_bone)
            if result is not None:
                head_proxies.append(result)

        self._ok(f"Head meshes: {len(head_proxies)}/{len(head_meshes)} berhasil.")
        return head_proxies, processed_colls

    # ------------------------------------------------------------------
    # Phase 7: Cleanup
    # ------------------------------------------------------------------
    def phase7_cleanup(self, processed_colls):
        self._banner("PHASE 7/7 : CLEANUP")
        for coll in processed_colls:
            for obj in coll.objects:
                if obj.type != 'MESH':
                    continue
                if obj.get(self.PROXY_HEAD_TAG_KEY):
                    pass  # Head proxy: keep modifiers & vertex groups
                else:
                    for m in list(obj.modifiers):
                        obj.modifiers.remove(m)
                    if obj.vertex_groups:
                        obj.vertex_groups.clear()
            coll.hide_render = False
        self._ok("Cleanup selesai.")

    # ------------------------------------------------------------------
    # Revert
    # ------------------------------------------------------------------
    def revert(self):
        self._banner("REVERT PROXYFY")
        self._ensure_object_mode()
        s = self.s

        source_names = set()
        proxy_objs = [o for o in bpy.data.objects if o.get(self.PROXY_TAG_KEY)]
        for po in proxy_objs:
            sn = po.get(self.PROXY_SOURCE_KEY)
            if sn:
                source_names.add(sn)
        for po in proxy_objs:
            self._safe_remove_object(po)
        self._log(f"[REV] {len(proxy_objs)} proxy dihapus.")

        for name in source_names:
            obj = bpy.data.objects.get(name)
            if obj is None:
                continue
            if obj.animation_data:
                for dp in ("hide_viewport", "hide_render"):
                    try:
                        obj.driver_remove(dp)
                    except Exception:
                        pass
            obj.hide_viewport = False
            obj.hide_render = False

        linked_hide = [o for o in bpy.data.objects
                       if o.get(self.PROXY_LINKED_TAG_KEY)]
        for obj in linked_hide:
            if obj.animation_data:
                for dp in ("hide_viewport", "hide_render"):
                    try:
                        obj.driver_remove(dp)
                    except Exception:
                        pass
            obj.hide_viewport = False
            obj.hide_render = False
            try:
                del obj[self.PROXY_LINKED_TAG_KEY]
            except Exception:
                pass

        for arm in bpy.data.objects:
            if arm.type != 'ARMATURE' or arm.pose is None:
                continue
            for bone_name in (s.control_bone_name,) + self.LEGACY_BONE_NAMES:
                pb = arm.pose.bones.get(bone_name)
                if pb is None:
                    continue
                for key in (s.prop_name,) + self.LEGACY_PROP_NAMES:
                    if key in pb:
                        try:
                            del pb[key]
                        except Exception:
                            pass

        for coll in list(bpy.data.collections):
            if (coll.name == "proxy_mesh"
                    and len(coll.objects) == 0
                    and len(coll.children) == 0):
                try:
                    bpy.data.collections.remove(coll)
                except Exception:
                    pass

        self._ok("Revert selesai.")

    # ------------------------------------------------------------------
    # Main entry
    # ------------------------------------------------------------------
    def run(self):
        self._banner("PROXYFY MK11 START")
        self._ensure_object_mode()

        (split_meshes, head_meshes, linked_hide_objs,
         control_arm, actual_bone) = self.phase1_preflight()

        self.phase2_validate_heads(head_meshes)
        self.phase3_create_property(control_arm, actual_bone)
        self.phase4_driver_source(
            split_meshes, head_meshes, linked_hide_objs, control_arm, actual_bone)

        all_proxy, colls_split = self.phase5_chunks_and_proxy_drivers(
            split_meshes, control_arm, actual_bone)

        head_proxies, colls_head = self.phase6_head_meshes(
            head_meshes, control_arm, actual_bone)

        self.phase7_cleanup(colls_split | colls_head)

        self._banner("PROXYFY MK11 SUMMARY")
        self._log(f"  Split meshes  : {len(split_meshes)} → {len(all_proxy)} chunks")
        self._log(f"  Head meshes   : {len(head_meshes)} → {len(head_proxies)} proxies")
        self._log(f"  [OK/WARN/ERR] : {self._counts['ok']} / "
                  f"{self._counts['warn']} / {self._counts['err']}")
        self._banner("SUCCESS")


# ---------------------------------------------------------------------------
# Operators
# ---------------------------------------------------------------------------

class PROXYFY_OT_run(Operator):
    bl_idname = "proxyfy.run"
    bl_label = "Run Proxyfy"
    bl_description = "Generate proxy meshes from selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        s = context.scene.proxyfy_settings
        core = _ProxyfyCore(context, s, self.report)
        try:
            core.run()
            self.report({'INFO'}, (
                f"Proxyfy done: "
                f"{core._counts['ok']} ok / "
                f"{core._counts['warn']} warn / "
                f"{core._counts['err']} err"
            ))
            return {'FINISHED'}
        except RuntimeError as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        finally:
            core.flush_log()


class PROXYFY_OT_revert(Operator):
    bl_idname = "proxyfy.revert"
    bl_label = "Revert Proxyfy"
    bl_description = "Remove all proxy objects and restore drivers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        s = context.scene.proxyfy_settings
        core = _ProxyfyCore(context, s, self.report)
        try:
            core.revert()
            self.report({'INFO'}, "Proxyfy reverted.")
            return {'FINISHED'}
        except RuntimeError as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        finally:
            core.flush_log()

# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

classes = (
    PROXYFY_OT_add_head_mesh,
    PROXYFY_OT_remove_head_mesh,
    PROXYFY_OT_add_linked_hide,
    PROXYFY_OT_remove_linked_hide,
    PROXYFY_OT_run,
    PROXYFY_OT_revert,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


# if __name__ == "__main__":
#     register()
