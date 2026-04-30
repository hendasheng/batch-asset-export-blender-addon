bl_info = {
    "name": "Batch Asset Export",
    "author": "OpenAI Codex",
    "version": (0, 1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Batch Asset Export",
    "description": "Batch export selected collection instances, meshes, curves, and realized GN results to OBJ and GLB",
    "category": "Import-Export",
}

import os
import re

import bpy
from bpy.props import BoolProperty, EnumProperty, PointerProperty, StringProperty
from bpy.types import Operator, Panel, PropertyGroup
from mathutils import Matrix


def is_zh_locale():
    locale = getattr(bpy.app.translations, "locale", "") or ""
    return locale.lower().startswith("zh")


def tr(zh_text: str, en_text: str) -> str:
    return zh_text if is_zh_locale() else en_text


translations_dict = {
    "zh_HANS": {
        ("*", "Batch Asset Export"): "批量资产导出",
        ("*", "Batch export selected collection instances, meshes, curves, and realized GN results to OBJ and GLB"): "批量导出选中的集合实例、网格、曲线和已实体化的几何节点结果为 OBJ 和 GLB",
        ("*", "OBJ Output"): "OBJ 输出目录",
        ("*", "Output folder for OBJ files"): "OBJ 文件输出目录",
        ("*", "GLB Output"): "GLB 输出目录",
        ("*", "Output folder for GLB files"): "GLB 文件输出目录",
        ("*", "Export OBJ"): "导出 OBJ",
        ("*", "Export GLB"): "导出 GLB",
        ("*", "Reset To Origin"): "位置归零",
        ("*", "Export selected objects with position reset to origin"): "导出时将选中对象的位置归零",
        ("*", "Export Selected"): "导出选中对象",
        ("*", "Export selected collection instances, meshes, curves, and realized GN objects"): "导出选中的集合实例、网格、曲线和已实体化的几何节点对象",
        ("*", "Batch Export"): "批量导出",
    },
    "zh_CN": {
        ("*", "Batch Asset Export"): "批量资产导出",
        ("*", "Batch export selected collection instances, meshes, curves, and realized GN results to OBJ and GLB"): "批量导出选中的集合实例、网格、曲线和已实体化的几何节点结果为 OBJ 和 GLB",
        ("*", "OBJ Output"): "OBJ 输出目录",
        ("*", "Output folder for OBJ files"): "OBJ 文件输出目录",
        ("*", "GLB Output"): "GLB 输出目录",
        ("*", "Output folder for GLB files"): "GLB 文件输出目录",
        ("*", "Export OBJ"): "导出 OBJ",
        ("*", "Export GLB"): "导出 GLB",
        ("*", "Reset To Origin"): "位置归零",
        ("*", "Export selected objects with position reset to origin"): "导出时将选中对象的位置归零",
        ("*", "Export Selected"): "导出选中对象",
        ("*", "Export selected collection instances, meshes, curves, and realized GN objects"): "导出选中的集合实例、网格、曲线和已实体化的几何节点对象",
        ("*", "Batch Export"): "批量导出",
    },
}


def safe_name(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', "_", name)


def show_message(message: str, title: str = "Batch Export"):
    def draw(self, _context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon="INFO")


def ensure_output_dir(path_value: str):
    if not path_value:
        return

    abs_path = bpy.path.abspath(path_value)
    if not abs_path:
        return

    try:
        os.makedirs(abs_path, exist_ok=True)
    except OSError:
        pass


def update_obj_export_dir(self, _context):
    ensure_output_dir(self.obj_export_dir)


def update_glb_export_dir(self, _context):
    ensure_output_dir(self.glb_export_dir)


def has_geometry_nodes_modifier(obj):
    return any(mod.type == "NODES" for mod in obj.modifiers)


def is_supported_geometry_object(obj):
    return obj.type in {"MESH", "CURVE"} or has_geometry_nodes_modifier(obj)


def collect_supported_objects_recursive(collection, parent_matrix=None):
    if parent_matrix is None:
        parent_matrix = Matrix.Identity(4)

    results = []

    for obj in collection.objects:
        local_matrix = parent_matrix @ obj.matrix_local.copy()

        if is_supported_geometry_object(obj):
            results.append((obj, local_matrix))
        elif obj.instance_type == "COLLECTION" and obj.instance_collection is not None:
            nested_parent = parent_matrix @ obj.matrix_local.copy()
            results.extend(
                collect_supported_objects_recursive(obj.instance_collection, nested_parent)
            )

    for child_collection in collection.children:
        results.extend(collect_supported_objects_recursive(child_collection, parent_matrix))

    return results


def duplicate_mesh_from_eval(context, source_obj, world_matrix, temp_name):
    depsgraph = context.evaluated_depsgraph_get()
    eval_obj = source_obj.evaluated_get(depsgraph)
    temp_mesh = bpy.data.meshes.new_from_object(eval_obj, depsgraph=depsgraph)
    if temp_mesh is None:
        return None

    temp_obj = bpy.data.objects.new(temp_name, temp_mesh)
    temp_obj.matrix_world = world_matrix
    context.scene.collection.objects.link(temp_obj)

    if hasattr(source_obj.data, "materials"):
        for material in source_obj.data.materials:
            temp_obj.data.materials.append(material)

    return temp_obj


def cleanup_temp_objects(temp_objects):
    for temp_obj in temp_objects:
        mesh = temp_obj.data
        bpy.data.objects.remove(temp_obj, do_unlink=True)
        if mesh and mesh.users == 0:
            bpy.data.meshes.remove(mesh)


def export_obj(context, temp_objects, filepath):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in temp_objects:
        obj.select_set(True)
    context.view_layer.objects.active = temp_objects[0]

    if hasattr(bpy.ops.wm, "obj_export"):
        return bpy.ops.wm.obj_export(
            filepath=filepath,
            export_selected_objects=True,
            export_materials=False,
        )

    return bpy.ops.export_scene.obj(
        filepath=filepath,
        use_selection=True,
        use_materials=False,
    )


def export_glb(context, temp_objects, filepath):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in temp_objects:
        obj.select_set(True)
    context.view_layer.objects.active = temp_objects[0]

    return bpy.ops.export_scene.gltf(
        filepath=filepath,
        use_selection=True,
        export_format="GLB",
        export_image_format="AUTO",
    )


class BATCHX_Properties(PropertyGroup):
    obj_export_dir: StringProperty(
        name="OBJ Output",
        description="Output folder for OBJ files",
        default="",
        update=update_obj_export_dir,
    )
    glb_export_dir: StringProperty(
        name="GLB Output",
        description="Output folder for GLB files",
        default="",
        update=update_glb_export_dir,
    )
    export_obj_enabled: BoolProperty(
        name="Export OBJ",
        default=True,
    )
    export_glb_enabled: BoolProperty(
        name="Export GLB",
        default=True,
    )
    reset_to_origin: BoolProperty(
        name="Reset To Origin",
        description="Export selected objects with position reset to origin",
        default=True,
    )


class BATCHX_OT_export_selected(Operator):
    bl_idname = "batchx.export_selected"
    bl_label = "Export Selected"
    bl_description = "Export selected collection instances, meshes, curves, and realized GN objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT" and context.selected_objects

    def execute(self, context):
        props = context.scene.batchx_props

        if not props.export_obj_enabled and not props.export_glb_enabled:
            self.report({"ERROR"}, tr("至少启用一种导出格式", "Enable at least one export format"))
            return {"CANCELLED"}

        if props.export_obj_enabled and not props.obj_export_dir.strip():
            message = tr("OBJ 输出目录为空，请先设置输出路径", "OBJ output path is empty. Set the output path first.")
            self.report({"ERROR"}, message)
            show_message(message)
            return {"CANCELLED"}

        if props.export_glb_enabled and not props.glb_export_dir.strip():
            message = tr("GLB 输出目录为空，请先设置输出路径", "GLB output path is empty. Set the output path first.")
            self.report({"ERROR"}, message)
            show_message(message)
            return {"CANCELLED"}

        obj_export_dir = bpy.path.abspath(props.obj_export_dir)
        glb_export_dir = bpy.path.abspath(props.glb_export_dir)

        if props.export_obj_enabled:
            os.makedirs(obj_export_dir, exist_ok=True)
        if props.export_glb_enabled:
            os.makedirs(glb_export_dir, exist_ok=True)

        selected_objects = list(context.selected_objects)
        original_active = context.view_layer.objects.active
        original_selection = list(context.selected_objects)
        exported_count = 0
        failures = []

        try:
            for inst in selected_objects:
                if inst.instance_type == "COLLECTION" and inst.instance_collection is not None:
                    object_entries = collect_supported_objects_recursive(
                        inst.instance_collection,
                        inst.matrix_world.copy(),
                    )
                    export_name = safe_name(inst.name)
                    if not object_entries:
                        failures.append(f"{inst.name}: collection has no mesh/curve/GN objects")
                        continue
                elif is_supported_geometry_object(inst):
                    object_entries = [(inst, inst.matrix_world.copy())]
                    export_name = safe_name(inst.name)
                else:
                    failures.append(f"{inst.name}: unsupported type {inst.type}")
                    continue

                temp_objects = []
                try:
                    for obj, nested_matrix in object_entries:
                        temp_name = f"{export_name}_TMP_{safe_name(obj.name)}"
                        world_matrix = nested_matrix.copy()
                        if props.reset_to_origin:
                            world_matrix.translation = (0.0, 0.0, 0.0)
                        temp_obj = duplicate_mesh_from_eval(context, obj, world_matrix, temp_name)
                        if temp_obj is None:
                            failures.append(f"{inst.name}/{obj.name}: could not create mesh")
                            continue
                        temp_objects.append(temp_obj)

                    if not temp_objects:
                        continue

                    if props.export_obj_enabled:
                        obj_filepath = os.path.join(obj_export_dir, export_name + ".obj")
                        export_obj(context, temp_objects, obj_filepath)

                    if props.export_glb_enabled:
                        glb_filepath = os.path.join(glb_export_dir, export_name + ".glb")
                        export_glb(context, temp_objects, glb_filepath)

                    exported_count += 1
                except Exception as exc:
                    failures.append(f"{inst.name}: {exc}")
                finally:
                    cleanup_temp_objects(temp_objects)
        finally:
            bpy.ops.object.select_all(action="DESELECT")
            for obj in original_selection:
                if obj.name in bpy.data.objects:
                    obj.select_set(True)
            if original_active and original_active.name in bpy.data.objects:
                context.view_layer.objects.active = original_active

        if failures:
            self.report(
                {"WARNING"},
                tr(
                    f"成功导出 {exported_count} 个，失败 {len(failures)} 个",
                    f"Exported {exported_count}, failed {len(failures)}",
                ),
            )
            show_message(
                tr(
                    f"成功导出 {exported_count} 个，失败 {len(failures)} 个。详情请查看控制台。",
                    f"Exported {exported_count}, failed {len(failures)}. Check console for details.",
                )
            )
            for item in failures[:20]:
                print("[Batch Export]", item)
        else:
            self.report(
                {"INFO"},
                tr(f"已导出 {exported_count} 个对象", f"Exported {exported_count} item(s)"),
            )
            show_message(tr(f"已导出 {exported_count} 个对象。", f"Exported {exported_count} item(s)."))

        return {"FINISHED"}


class BATCHX_OT_pick_directory(Operator):
    bl_idname = "batchx.pick_directory"
    bl_label = "Pick Directory"
    bl_description = "Choose an output directory"

    target: EnumProperty(
        name="Target",
        items=(
            ("OBJ", "OBJ", ""),
            ("GLB", "GLB", ""),
        ),
    )
    directory: StringProperty(subtype="DIR_PATH")

    def execute(self, context):
        props = context.scene.batchx_props
        if self.target == "OBJ":
            props.obj_export_dir = self.directory
        else:
            props.glb_export_dir = self.directory
        return {"FINISHED"}

    def invoke(self, context, _event):
        props = context.scene.batchx_props
        self.directory = props.obj_export_dir if self.target == "OBJ" else props.glb_export_dir
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class BATCHX_PT_panel(Panel):
    bl_label = "Batch Asset Export"
    bl_idname = "BATCHX_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Batch Export"

    def draw(self, context):
        layout = self.layout
        props = context.scene.batchx_props
        layout.use_property_split = False
        layout.use_property_decorate = False

        path_box = layout.box()
        path_col = path_box.column(align=False)
        path_col.label(text=tr("导出目标", "Export Targets"), icon="FILE_FOLDER")
        path_col.separator(factor=0.45)
        obj_col = path_col.column(align=False)
        obj_toggle_row = obj_col.row(align=True)
        obj_toggle_row.prop(props, "export_obj_enabled", text=tr("导出 OBJ", "Export OBJ"))
        obj_col.separator(factor=0.2)
        obj_row = obj_col.row(align=True)
        obj_row.enabled = props.export_obj_enabled
        obj_row.prop(props, "obj_export_dir", text="")
        obj_op = obj_row.operator("batchx.pick_directory", text="", icon="FILE_FOLDER")
        obj_op.target = "OBJ"
        path_col.separator(factor=0.35)
        glb_col = path_col.column(align=False)
        glb_toggle_row = glb_col.row(align=True)
        glb_toggle_row.prop(props, "export_glb_enabled", text=tr("导出 GLB", "Export GLB"))
        glb_col.separator(factor=0.2)
        glb_row = glb_col.row(align=True)
        glb_row.enabled = props.export_glb_enabled
        glb_row.prop(props, "glb_export_dir", text="")
        glb_op = glb_row.operator("batchx.pick_directory", text="", icon="FILE_FOLDER")
        glb_op.target = "GLB"

        layout.separator(factor=0.4)

        settings_box = layout.box()
        settings_col = settings_box.column(align=False)
        settings_col.label(text=tr("导出设置", "Export Settings"), icon="SETTINGS")
        settings_col.separator(factor=0.45)

        transform_col = settings_col.column(align=True)
        transform_col.label(text=tr("变换", "Transform"))
        transform_col.prop(props, "reset_to_origin")

        layout.separator(factor=0.4)

        info_box = layout.box()
        info_col = info_box.column(align=False)
        info_col.label(text=tr("支持对象", "Supported"), icon="INFO")
        info_col.separator(factor=0.45)
        info_col.label(text=tr("集合实例", "Collection Instance"))
        info_col.label(text=tr("网格 / 曲线", "Mesh / Curve"))
        info_col.label(text=tr("已实体化几何节点", "Realized Geometry Nodes"))

        layout.separator(factor=0.4)

        note_box = layout.box()
        note_col = note_box.column(align=False)
        note_col.label(text=tr("注意事项", "Notes"), icon="ERROR")
        note_col.separator(factor=0.45)
        note_col.label(text=tr("每个项目先检查输出路径", "Set output paths per project"))
        note_col.label(text=tr("几何节点导出为空时先实现实例", "Realize GN instances if export is empty"))

        layout.separator(factor=0.5)

        action_box = layout.box()
        action_col = action_box.column(align=True)
        action_col.scale_y = 1.45
        action_row = action_col.row(align=True)
        action_row.operator(
            "batchx.export_selected",
            text=tr("导出选中对象", "Export Selected"),
            icon="EXPORT",
        )


classes = (
    BATCHX_Properties,
    BATCHX_OT_export_selected,
    BATCHX_OT_pick_directory,
    BATCHX_PT_panel,
)


def register():
    bpy.app.translations.register(__name__, translations_dict)
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.batchx_props = PointerProperty(type=BATCHX_Properties)
    try:
        ensure_output_dir(bpy.context.scene.batchx_props.obj_export_dir)
        ensure_output_dir(bpy.context.scene.batchx_props.glb_export_dir)
    except Exception:
        pass


def unregister():
    del bpy.types.Scene.batchx_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.app.translations.unregister(__name__)


if __name__ == "__main__":
    register()
