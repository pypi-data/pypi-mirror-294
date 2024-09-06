import os
import re
import glob
import time
import pathlib
import tempfile
import json
from kabaret import flow
from kabaret.app import resources
from kabaret.flow_contextual_dict import get_contextual_dict
from libreflow.baseflow import ProjectSettings
from libreflow.baseflow.file import GenericRunAction, LinkedJob, AERenderSettings, AEOutputModule
from libreflow.baseflow.task import Task
from libreflow.utils.kabaret.jobs.jobs_flow import Job, Jobs
from libreflow.resources.icons import gui as _
from libreflow.resources import file_templates as _
from .build_utils import wrap_python_expr
from .error_handlers import ErrorHandlers
from . import scripts

from . import _version
__version__ = _version.get_versions()['version']


def get_jsx_build_script(jsx_import_script_path, scene_path):
    layer_list_path = jsx_import_script_path.replace(".jsx", "_layers.list")
    jsx_setup_path = resources.get('scripts', 'setup_comp.jsx')
    jsx_tmp_fd, jsx_tmp_path = tempfile.mkstemp(suffix='.jsx')
    with open(jsx_import_script_path, 'r', encoding='utf-8-sig') as jsx_import, \
         open(jsx_setup_path, 'r', encoding='utf-8-sig') as jsx_setup, \
         open(layer_list_path, 'r', encoding='utf-8-sig') as layer_list, \
         open(jsx_tmp_fd, 'a') as jsx_tmp:
        # Write original jsx importer created by Blender
        jsx_tmp.write(jsx_import.read())
        jsx_tmp.write('\n')

        # Write list of layers
        # layer_list = [f'"{line}"' for line in layer_list.read().split()]
        layer_list = layer_list.read().split()
        jsx_tmp.write("layersList = ")
        jsx_tmp.write(json.dumps(layer_list, indent=4))
        jsx_tmp.write(';\n')

        # Write post-import script
        jsx_tmp.write(jsx_setup.read())
        jsx_tmp.write(f"\nvar file = File('{scene_path}');\n")
        jsx_tmp.write("app.project.save(file);\n")
        jsx_tmp.close()
    return jsx_tmp_path


class AssetStatus(flow.values.ChoiceValue):

    CHOICES = ["NotAvailable", "Downloadable", "Available"]


class TaskFileDependency(flow.Object):

    _parent = flow.Parent()
    _shot = flow.Parent(3)

    asset_type = flow.Computed(store_value=False)
    asset_family = flow.Computed(store_value=False)
    asset_code = flow.Computed(store_value=False)
    asset_number = flow.Computed(store_value=False)
    asset_path = flow.Computed(store_value=False)
    asset_oid = flow.Computed(store_value=False)
    asset_file_oid = flow.Computed(store_value=False)
    asset_revision_oid = flow.Computed(store_value=False)
    available = flow.Computed(store_value=False)

    def compute_child_value(self, child_value):
        asset_data = self._parent.asset_data(self.name())

        if child_value is self.asset_type:
            child_value.set(asset_data['asset_type'])
        elif child_value is self.asset_family:
            child_value.set(asset_data['asset_family'])
        elif child_value is self.asset_number and 'asset_number' in asset_data:
            child_value.set(asset_data['asset_number'])
        elif child_value is self.asset_oid:
            if self.name() == "animatic":
                oid = self._shot.oid()
            else:
                asset_type = self.asset_type.get()
                asset = None
                asset_family = self.asset_family.get()
                asset_name = self.name()
                oid = self.root().project().oid() + f"/asset_types/{asset_type}/asset_families/{asset_family}/assets/{asset_name}"
                if not self.root().session().cmds.Flow.exists(oid): # ensure asset exists
                    self.root().session().log_warning(f'Scene Builder - undefined asset {oid}')
                    oid = None
            child_value.set(oid)
        elif child_value is self.asset_file_oid:
            asset_type = self.asset_type.get()
            asset_oid = self.asset_oid.get()

            if asset_oid is not None:
                asset = self.root().get_object(asset_oid)
            else:
                child_value.set(None)
                return

            file_name = self._parent.asset_type_file_name(asset_type)
            files = self._parent.files_from_asset_type(asset, asset_type)

            if files is None or not files.has_mapped_name(file_name):
                child_value.set(None)
            else:
                child_value.set(files[file_name].oid())
        elif child_value is self.asset_code:
            oid = self.asset_oid.get()
            if oid is None:
                child_value.set(None)
            else:
                asset = self.root().get_object(oid)
                child_value.set(asset.code.get())
        elif child_value is self.asset_revision_oid:
            asset_file_oid = self.asset_file_oid.get()

            if asset_file_oid:
                file = self.root().get_object(asset_file_oid)
                rev = file.get_head_revision()

                if rev and rev.exists():
                    child_value.set(rev.oid())
                else:
                    child_value.set(None)
            else:
                child_value.set(None)
        elif child_value is self.asset_path:
            asset_revision_oid = self.asset_revision_oid.get()
            asset_type = self.asset_type.get()

            if not asset_revision_oid:
                child_value.set(None)
            else:
                rev = self.root().get_object(asset_revision_oid)
                if not rev.exists():
                    child_value.set(None)
                else:
                    child_value.set(rev.get_path())
        elif child_value is self.available:
            asset_path = self.asset_path.get()

            if self.asset_revision_oid.get():
                child_value.set("Available")
            elif self.asset_file_oid.get():
                child_value.set("Downloadable")
            else:
                child_value.set("NotAvailable")


class RefreshDependencies(flow.Action):
    ICON = ('icons.gui', 'refresh')
    _map = flow.Parent()

    def needs_dialog(self):
        return False

    def run(self, button):
        self._map.refresh()


class TaskFileDependencies(flow.DynamicMap):
    refresh_action = flow.Child(RefreshDependencies).ui(
        label="Refresh")
    _task = flow.Parent(2)
    _shot = flow.Parent(4)
    _sequence = flow.Parent(6)
    _updated = flow.BoolParam(False)

    def __init__(self, parent, name):
        super(TaskFileDependencies, self).__init__(parent, name)
        self._assets_data_time = time.time()
        self._assets_data = None

    def mapped_names(self, page_num=0, page_size=None):
        if not self._assets_data or time.time() - self._assets_data_time > 30.0:
            self._assets_data = self._get_assets_data()
            self._assets_data_time = time.time()

        return list(self._assets_data.keys())

    def get_kitsu_casting(self, casting):
        kitsu_api = self.root().project().kitsu_api()
        kitsu_casting = kitsu_api.get_shot_casting(self._shot.name(), self._sequence.name())
        if kitsu_casting is None:
            return

        # Kitsu assets
        for asset in kitsu_casting:
            asset_name = asset['asset_name']
            asset_type = asset['asset_type_name']
            asset_family = kitsu_api.get_asset_data(asset_name)['data'].get('category', asset_type.lower())

            casting[asset_name.replace('-', '_')] = dict(
                asset_type=asset_type.lower(),
                asset_family=asset_family.lower(),
                asset_number=asset['nb_occurences']
            )

    def get_animatic_casting(self, casting):
        # Animatic
        casting['animatic'] = dict(
            asset_type='animatic',
            asset_family='',
        )

    def _get_assets_data(self):
        raise NotImplementedError

    def asset_data(self, asset_name):
        return self._assets_data[asset_name]

    @classmethod
    def mapped_type(cls):
        return TaskFileDependency

    def columns(self):
        return ["Name", "Type", "Family", "Revision"]

    def asset_type_file_name(self, asset_type):
        return {
            "sets": "layers",
            "animals": "rigging_blend",
            "characters": "rigging_blend",
            "props": "rigging_blend",
            "animatic": "animatic_mov",
        }[asset_type]

    def files_from_asset_type(self, asset, asset_type):
        if asset_type == 'sets' and asset.tasks.has_mapped_name('design'):
            return asset.tasks['design'].files
        elif asset_type == 'animatic':
            return asset.files
        elif asset.tasks.has_mapped_name('rigging'):
            return asset.tasks['rigging'].files
        else:
            return None

    def refresh(self):
        self._assets_data = None
        self.touch()

    def _fill_row_cells(self, row, item):
        row["Name"] = item.name()
        row["Type"] = item.asset_type.get()
        row["Family"] = item.asset_family.get()

        rev_oid = item.asset_revision_oid.get()
        rev_name = rev_oid.split("/")[-1] if rev_oid else ""
        row["Revision"] = rev_name

    def _fill_row_style(self, style, item, row):
        icon_by_status = {
            "NotAvailable": ("icons.libreflow", "cross-mark-on-a-black-circle-background-colored"),
            "Downloadable": ("icons.libreflow", "exclamation-sign-colored"),
            "Available": ("icons.libreflow", "checked-symbol-colored"),
        }
        style["icon"] = icon_by_status[item.available.get()]


class BuildBlenderScene(GenericRunAction):
    ICON = ('icons.libreflow', 'blender')

    _task = flow.Parent()
    _shot = flow.Parent(3)
    _sequence = flow.Parent(5)

    def runner_name_and_tags(self):
        return 'Blender', []

    def get_run_label(self):
        return "Build scene"

    def get_buttons(self):
        # Make build action behave as base RunAction by default
        return RunAction.get_buttons(self)

    def needs_dialog(self):
        return True

    def extra_env(self):
        return {
            "ROOT_PATH": self.root().project().get_root()
        }

    def target_file_extension(self):
        return 'blend'

    def get_template_path(self, default_file):
        template_oid = default_file.template_file.get()
        if template_oid is None or not self.root().session().cmds.Flow.exists(template_oid): # check file template
            print(f'Scene Builder -  template of {self._task.name()}/{default_file.name()} is undefined -> use default template')
            return template_path

        template = self.root().get_object(template_oid)
        if template is None: # check file template
            print(f'Scene Builder - template of {self._task.name()}/{default_file.name()} is undefined -> use default template')
            return template_path

        rev_name = default_file.template_file_revision.get()
        if rev_name == 'Latest': # check template revision
            rev = template.get_head_revision()
        else:
            rev = template.get_revision(rev_name)
        if rev is None or rev.get_sync_status() != 'Available':
            print(f'Scene Builder - template of {self._task.name()}/{default_file.name()} is not available -> use default template')
            return template_path

        rev_path = rev.get_path()
        if not os.path.exists(rev_path):
            print(f'Scene Builder - template of {self._task.name()}/{default_file.name()} is not available -> use default template')
            return template_path

        print(f'Scene Builder - custom template found: {self._task.name()}/{default_file.name()} -> {rev_path}')
        return rev_path

    def get_default_file(self, task_name, filename):
        file_mapped_name = filename.replace('.', '_')
        template_path = resources.get("file_templates", "template.blend")
        mng = self.root().project().get_task_manager()
        if not mng.default_tasks.has_mapped_name(task_name): # check default task
            # print(f'Scene Builder - no default task {task_name} -> use default template')
            return None

        dft_task = mng.default_tasks[task_name]
        if not dft_task.files.has_mapped_name(file_mapped_name): # check default file
            # print(f'Scene Builder - default task {task_name} has no default file {filename} -> use default template')
            return None

        dft_file = dft_task.files[file_mapped_name]
        return dft_file

    def get_path_format(self, task_name, filename):
        dft_file = self.get_default_file(task_name, filename)
        if dft_file is None:
            return None

        return dft_file.path_format.get()

    def _ensure_file(self, name, format, path_format,
                     folder=False, to_edit=False,
                     src_path=None, publish_comment="",
                     task=None, file_type=None):
        if task is None:
            task = self._task

        files = task.files
        file_name = "%s_%s" % (name, format)

        if files.has_file(name, format):
            file = files[file_name]
        else:
            file = files.add_file(
                name=name,
                extension=format,
                tracked=True,
                default_path_format=path_format,
            )

        if not to_edit and not src_path:
            return None

        if to_edit:
            revision = file.create_working_copy(source_path=src_path)
        else:
            revision = file.publish(source_path=src_path, comment=publish_comment)

        if file_type is not None:
            file.file_type.set(file_type)

        return revision.get_path()

    def _ensure_folder(self, name, path_format,
                       to_edit=False,
                       src_path=None, publish_comment="",
                       task=None, file_type=None):
        if task is None:
            task = self._task

        files = task.files

        if files.has_folder(name):
            folder = files[name]
        else:
            folder = files.add_folder(
                name=name,
                tracked=True,
                default_path_format=path_format,
            )

        # XXX Could we publish without creating a working copy?
        folder.create_working_copy(path_format=path_format)
        if not to_edit:
            revision = folder.publish(comment=publish_comment)

        if file_type is not None:
            folder.file_type.set(file_type)

        return revision.get_path()

    def _blender_cmd(self, operator, **kwargs):
        '''
        Returns Blender scene builder operator command as a string.

        Operator must be one of the following:
        `setup`, `setup_anim`,
        `add_asset`, `add_set`,
        `add_animatic`, `update_animatic`,
        `add_audio`, `add_board`, (deprecated, use add_animatic instead)
        `update_audio`, `update_board`, (deprecated, use update_animatic instead without args)
        `export_ae`, `setup_render`,
        'create_collections', 'setup_render_layers', 'setup_render_node_tree',
        `cleanup`, `save`.
        '''

        blender_operators = {
            "setup": {'operator_command': "bpy.ops.pipeline.scene_builder_setup",
                      'args': "frame_start={frame_start}, frame_end={frame_end}, resolution_x={resolution_x}, resolution_y={resolution_y}, fps={fps}, create_camera=False"},
            "setup_anim": {'operator_command': "bpy.ops.pipeline.scene_builder_setup_animation",
                           'args': 'alembic_filepath="{alembic_filepath}", assets={assets}, create_ghost={create_ghost}'},

            "add_asset": {'operator_command': 'bpy.ops.pipeline.scene_builder_import_asset',
                          'args': 'filepath="{filepath}", asset_name="{asset_name}", target_collection="{asset_type}"'},
            "add_animatic": {'operator_command': 'bpy.ops.pipeline.scene_builder_add_animatic',
                             'args': 'filepath="{filepath}"'},
            "add_set": {'operator_command': 'bpy.ops.pipeline.scene_builder_import_set',
                        'args': 'directory="{set_dir}", files={set_dicts}'},
            "add_audio": {'operator_command': 'bpy.ops.pipeline.scene_builder_import_audio',
                          'args': 'filepath="{filepath}"'},
            "add_board": {'operator_command': 'bpy.ops.pipeline.scene_builder_import_storyboard',
                          'args': 'filepath="{filepath}", use_corner={use_corner}'},

            "update_animatic": {'operator_command': 'bpy.ops.pipeline.scene_builder_update_animatic',
                                'args': ''},
            "update_audio": {'operator_command': 'bpy.ops.pipeline.scene_builder_update_audio',
                             'args': ''},
            "update_board": {'operator_command': 'bpy.ops.pipeline.scene_builder_update_storyboard',
                             'args': 'filepath="{filepath}"'},

            "export_ae": {'operator_command': 'bpy.ops.pipeline.scene_builder_export_ae',
                          'args': 'filepath="{filepath}"'},

            "setup_render": {'operator_command': "bpy.ops.pipeline.scene_builder_setup_render",
                             'args': 'kitsu_duration={kitsu_duration}'},

            "create_collections": {'operator_command': "bpy.ops.pipeline.setup_render_create_collections",
                                   'args': ''},
            "setup_render_layers": {'operator_command': "bpy.ops.pipeline.setup_render_layers",
                                    'args': ''},
            "setup_render_node_tree": {'operator_command': "bpy.ops.pipeline.setup_render_node_tree",
                                       'args': '"EXEC_DEFAULT", directory="{directory}"'},

            "cleanup": {'operator_command': 'bpy.ops.pipeline.scene_builder_cleanup',
                        'args': ''},
            "save": {'operator_command': 'bpy.ops.wm.save_mainfile',
                     'args': 'filepath="{filepath}", compress=True'},
        }

        op = blender_operators[operator]
        operator_command = op['operator_command']
        args = op['args'].format(**kwargs)
        command = f"if {operator_command}.poll(): {operator_command}({args})\n"
        return command


class LayoutDependencies(TaskFileDependencies):

    def _get_assets_data(self):
        casting = dict()
        self.get_kitsu_casting(casting)
        self.get_animatic_casting(casting)
        return casting


class BuildLayoutScene(BuildBlenderScene):

    dependencies = flow.Child(LayoutDependencies).ui(expanded=True)

    def get_run_label(self):
        return 'Build layout scene'

    def extra_argv(self):
        # Get scene builder arguments
        frame_start = 101
        frame_end = 101 + self._shot_data["nb_frames"] - 1
        resolution_x = 2048
        resolution_y = 858
        fps = 24

        assets = self._shot_data["assets_data"]
        sets = self._shot_data["sets_data"]
        animatic_path = self._shot_data.get("animatic_path", None)
        layout_path = self._shot_data["layout_scene_path"] # Mandatory
        template_path = self._shot_data.get("layout_template_path", \
            resources.get("file_templates", "template.blend"))

        # Build Blender Python expression
        python_expr = "import bpy\n"
        python_expr += self._blender_cmd("setup", frame_start=frame_start, frame_end=frame_end,
                                         resolution_x=resolution_x, resolution_y=resolution_y, fps=fps)
        python_expr += self._blender_cmd("save", filepath=layout_path)

        for name, path, asset_type, asset_number in assets:
            for i in range(asset_number):
                python_expr += self._blender_cmd(
                    "add_asset", filepath=path, asset_name=name, asset_type=asset_type)
        for set_dir, set_dicts in sets:
            python_expr += self._blender_cmd("add_set",
                                             set_dir=set_dir, set_dicts=set_dicts)
        if animatic_path:
            python_expr += self._blender_cmd("add_animatic",
                                             filepath=animatic_path)

        # python_expr += self._blender_cmd("cleanup")
        python_expr += self._blender_cmd("save", filepath=layout_path)

        return [
            "-b", template_path,
            "--addons", "io_import_images_as_planes,camera_plane,lfs_scene_builder,add_camera_rigs",
            "--python-expr", wrap_python_expr(python_expr)
        ]

    def get_buttons(self):
        msg = "<h2>Build layout shot</h2>"

        for dep in self.dependencies.mapped_items():
            if dep.available.get() in ["Downloadable", "NotAvailable"]:
                msg += (
                    "<h3><font color=#D66700>"
                    "Some dependencies are still missing, either because they do not already exists or need to be downloaded on your site.\n"
                    "You can build the scene anyway, but you will have to manually update it when missing dependencies will be available."
                    "</font></h3>"
                )
                break

        self.message.set(msg)

        return ["Build and edit", "Build and publish", "Cancel"]

    def run(self, button):
        if button == "Cancel":
            return

        if button == "Refresh":
            self.dependencies.touch()
            return self.get_result(refresh=True, close=False)

        shot_name = self._shot.name()
        sequence_name = self._sequence.name()

        # Get shot data
        kitsu_api = self.root().project().kitsu_api()
        shot_data = kitsu_api.get_shot_data(shot_name, sequence_name)

        # Store dependencies file paths for Blender script building
        self._shot_data = {}
        self._shot_data["nb_frames"] = shot_data["nb_frames"]
        if self._shot_data["nb_frames"] is None:
            self._shot_data["nb_frames"] = 0
        self._shot_data["assets_data"] = []
        self._shot_data["sets_data"] = []

        for dep in self.dependencies.mapped_items():
            if dep.available.get() != "Available":
                continue

            asset_type = dep.asset_type.get()
            asset_number = dep.asset_number.get()
            path = dep.asset_path.get().replace("\\", "/")
            path = re.sub(r"^//([^/]+)/", r"\\\\\\\\\1\\\\", path) # check drive name
            if asset_type == "sets":
                set_path = re.sub(r"^\\\\\\\\([^/]+)\\\\", r"\\\\\1\\", path) # revert set path to find images
                set_names = list(map(os.path.basename, glob.glob("%s/*.png" % set_path)))
                self._shot_data["sets_data"].append(
                    (path, [{"name": name} for name in set_names])
                )
            elif asset_type == "animatic":
                self._shot_data["animatic_path"] = path
            else: # characters/props/animals
                self._shot_data["assets_data"].append((dep.asset_code.get(), path, asset_type, asset_number))

        # Get layout file preset to resolve template and path format
        default_file = self.get_default_file(self._task.name(), "layout.blend")
        path_format = None
        if default_file is not None:
            self._shot_data["layout_template_path"] = self.get_template_path(default_file)
            path_format = default_file.path_format.get()
        # Configure layout file
        layout_path = self._ensure_file(
            name='layout',
            format='blend',
            path_format=path_format,
            to_edit=(button == 'Build and edit'),
            src_path=resources.get("file_templates", "template.blend"),
            publish_comment="Created with scene builder"
        )

        self._task.touch()

        # Store layout output path
        layout_path = layout_path.replace("\\", "/")
        layout_path = re.sub(r"^//([^/]+)/", r"\\\\\\\\\1\\\\", layout_path) # check drive name
        self._shot_data["layout_scene_path"] = layout_path

        # Build
        super(BuildLayoutScene, self).run(button)


class BlockingDependencies(TaskFileDependencies):

    def _get_assets_data(self):
        casting = dict()
        self.get_kitsu_casting(casting)
        return casting


class BuildBlockingScene(BuildBlenderScene):

    dependencies = flow.Child(BlockingDependencies).ui(expanded=True)

    create_ghost = flow.SessionParam(True).ui(editor='bool')

    def get_run_label(self):
        return 'Build blocking scene'

    def extra_argv(self):
        # Get scene builder arguments
        anim_path = self._shot_data.get("anim_path", None)
        alembic_path = self._shot_data.get("alembic_path", None)
        assets_data = self._shot_data.get("assets_data", [])
        assets = []
        create_ghost = self.create_ghost.get()

        for name, path, asset_type, asset_number in assets_data:
            for i in range(asset_number):
                assets.append({"name": name,
                               "filepath": path,
                               "target_collection": asset_type})

        # Build Blender Python expression
        python_expr = "import bpy\n"
        python_expr += self._blender_cmd("setup_anim",
                                         alembic_filepath=alembic_path, assets=assets, create_ghost=create_ghost)

        # Update reference files
        python_expr += self._blender_cmd("update_animatic")

        python_expr += self._blender_cmd("cleanup")
        python_expr += self._blender_cmd("save", filepath=anim_path)

        return [
            "-b", anim_path,
            "--addons", "io_import_images_as_planes,camera_plane,lfs_scene_builder,add_camera_rigs",
            "--python-expr", wrap_python_expr(python_expr)
        ]

    def get_buttons(self):
        latest_revision = None
        files = self._shot.tasks['layout'].files

        if "layout_blend" in files.mapped_names():
            latest_revision = files["layout_blend"].get_head_revision()

        if (latest_revision is None or latest_revision.get_sync_status() != 'Available'):
            msg = "<h2><font color=#D5000D>Last revision of layout file not available</font></h2>"
            buttons = ["Cancel"]
        else:
            msg = "<h2>Build animation shot</h2>"
            buttons = ["Build and edit", "Cancel"]

            for dep in self.dependencies.mapped_items():
                if dep.available.get() in ["Downloadable", "NotAvailable"]:
                    msg += (
                        "<h3><font color=#D66700>"
                        "Some dependencies are still missing, either because they do not already exists or need to be downloaded on your site.\n"
                        "You can build the scene anyway, but you will have to manually update it when missing dependencies will be available."
                        "</font></h3>"
                    )
                    break

        self.message.set(msg)

        return buttons

    def run(self, button):
        if button == 'Cancel':
            return

        if button == "Refresh":
            self.dependencies.touch()
            return self.get_result(refresh=True, close=False)

        # Store dependencies file paths for Blender script building
        self._shot_data = {}
        self._shot_data["assets_data"] = []

        for dep in self.dependencies.mapped_items():
            if dep.available.get() != "Available":
                continue

            asset_type = dep.asset_type.get()
            asset_number = dep.asset_number.get()
            path = dep.asset_path.get().replace("\\", "/")
            path = re.sub(r"^//([^/]+)/", r"\\\\\1\\", path)  # check drive name

            if asset_type in ["sets", "animatic"]:
                continue
            self._shot_data["assets_data"].append((dep.asset_code.get(), path, asset_type, asset_number))

        # Configure anim file
        latest_revision = self._shot.tasks['layout'].files["layout_blend"].get_head_revision()
        layout_path = latest_revision.get_path()

        # Create empty file
        anim_path = self._ensure_file(
            name='anim_blocking',
            format='blend',
            path_format=self.get_path_format(self._task.name(), 'anim_blocking.blend'),
            to_edit=True,
            src_path=layout_path,
            publish_comment="Created with anim scene builder"
        )

        create_ghost = self.create_ghost.get()
        if create_ghost:
            # Configure alembic file
            alembic_path = self._ensure_file(
                name='ref_layout',
                format='abc',
                path_format=self.get_path_format(self._task.name(), 'ref_layout.abc'),
                src_path=resources.get("file_templates", "template.abc"),
                publish_comment="Created with anim scene builder"
            )

        # Store anim and alembic output path
        anim_path = anim_path.replace("\\", "/")
        anim_path = re.sub(r"^//([^/]+)/", r"\\\\\\\\\1\\\\", anim_path)  # check drive name
        self._shot_data["anim_path"] = anim_path

        if create_ghost:
            alembic_path = alembic_path.replace("\\", "/")
            alembic_path = re.sub(r"^//([^/]+)/", r"\\\\\\\\\1\\\\", alembic_path)  # check drive name
            self._shot_data["alembic_path"] = alembic_path

        # Build
        super(BuildBlockingScene, self).run(button)


class BuildRenderScene(BuildBlenderScene):

    _tasks = flow.Parent(2)

    def get_run_label(self):
        return 'Build rendering scene'

    def extra_argv(self):
        # Get scene builder arguments
        render_path = self._shot_data.get("render_path", None)
        jsx_path = self._shot_data.get("jsx_path", None)
        passes_path = self._shot_data.get("passes_path", None)
        shot_duration = self._shot_data.get("nb_frames", 0)

        # Build Blender Python expression
        # TODO actual render setup
        python_expr = "import bpy\n"
        python_expr += self._blender_cmd("setup_render", kitsu_duration=shot_duration)
        python_expr += self._blender_cmd("cleanup")
        python_expr += self._blender_cmd("create_collections")
        python_expr += self._blender_cmd("setup_render_layers")
        python_expr += self._blender_cmd("setup_render_node_tree", directory=passes_path)
        python_expr += self._blender_cmd("save", filepath=render_path)

        python_expr += self._blender_cmd("export_ae", filepath=jsx_path)

        return [
            "-b", render_path,
            "--addons", "io_import_images_as_planes,camera_plane,lfs_scene_builder,add_camera_rigs",
            "--python-expr", wrap_python_expr(python_expr)
        ]

    def get_buttons(self):
        latest_revision = None
        files = self._shot.tasks['animspline'].files

        if "anim_spline_blend" in files.mapped_names():
            latest_revision = files["anim_spline_blend"].get_head_revision()

        if (latest_revision is None or latest_revision.get_sync_status() != 'Available'):
            msg = "<h2><font color=#D5000D>Last revision of layout file not available</font></h2>"
            buttons = ["Cancel"]
        else:
            msg = "<h2>Build render shot</h2>"
            buttons = ["Build", "Cancel"]

        self.message.set(msg)

        return buttons

    def run(self, button):
        if button == 'Cancel':
            return

        shot_name = self._shot.name()
        sequence_name = self._sequence.name()

        # Store dependencies file paths for Blender script building
        self._shot_data = {}

        # Configure render file
        latest_revision = self._shot.tasks['animspline'].files["anim_spline_blend"].get_head_revision()
        layout_path = latest_revision.get_path()

        # Create empty file
        render_path = self._ensure_file(
            name='rendering',
            format='blend',
            path_format=self.get_path_format(self._task.name(), 'rendering.blend'),
            src_path=layout_path,
            publish_comment="Created with render scene builder"
        )

        # Configure jsx file
        jsx_path = self._ensure_file(
            name='compositing',
            format='jsx',
            path_format=self.get_path_format(self._task.name(), 'compositing.jsx'),
            src_path=resources.get("file_templates", "template.jsx"),
            publish_comment="Export from Blender",
            file_type="Outputs",
        )

        # Get comp department to create remaining files there
        if not self._tasks.has_mapped_name("comp"):
            print("COMP NOT FOUND")
            return

        comp_task = self._tasks["comp"]

        # Configure AE file
        aep_path = self._ensure_file(
            name='compositing',
            format='aep',
            path_format=self.get_path_format(comp_task.name(), 'compositing.aep'),
            to_edit=True,
            src_path=resources.get("file_templates", "template.aep"),
            task=comp_task,
        )

        # Configure render dir
        passes_path = self._ensure_folder(
            name='passes',
            path_format=self.get_path_format(comp_task.name(), 'passes'),
            publish_comment="Render",
            task=comp_task,
            file_type="Inputs",
        )

        # Store output paths
        render_path = render_path.replace("\\", "/")
        render_path = re.sub(r"^//([^/]+)/", r"\\\\\\\\\1\\\\", render_path)  # check drive name
        self._shot_data["render_path"] = render_path

        jsx_path = jsx_path.replace("\\", "/")
        jsx_path = re.sub(r"^//([^/]+)/", r"\\\\\\\\\1\\\\", jsx_path)  # check drive name
        self._shot_data["jsx_path"] = jsx_path

        aep_path = aep_path.replace("\\", "/")
        aep_path = re.sub(r"^//([^/]+)/", r"\\\\\\\\\1\\\\", aep_path)  # check drive name
        self._shot_data["aep_path"] = aep_path

        passes_path = passes_path.replace("\\", "/")
        passes_path = re.sub(r"^//([^/]+)/", r"\\\\\\\\\1\\\\", passes_path)  # check drive name
        self._shot_data["passes_path"] = passes_path

        # Build
        return super(BuildRenderScene, self).run(button)


class TaskJob(LinkedJob):

    def get_log_filename(self):
        d = get_contextual_dict(self, 'settings')
        filename = f"{d['film']}_{d['sequence']}_{d['shot']}_{d['task']}_{self.name()}_{self.job_id.get()}.job_log"
        log_path = pathlib.Path.home()/f".libreflow/log/jobs/{self.root().project().name()}/{filename}"
        return log_path

    def is_running(self, runner_id):
        info = self.root().session().cmds.SubprocessManager.get_runner_info(
            runner_id)
        return info['is_running']

    def show_runner_info(self, runner_info, description=None):
        if description is not None:
            description = "- "+description
        else:
            description = ""
        self.show_message(f"[INFO] Runner {runner_info['id']} started...")
        self.show_message(f"[INFO] Description: {runner_info['label']} {description}")
        self.show_message(f"[INFO] Command: {runner_info['command']}")
        self.show_message(f"[INFO] Log path: {runner_info['log_path']}")

    def check_process_errors(self, log_path, runner_name, label):
        """
        Check for errors in the given log file path matched by
        error handlers associated to the given runner name.
        """
        self.show_message("Checking for errors...")
        handlers = self.root().project().admin.project_settings.runner_error_handlers
        msg = None
        error = None
        for handler in handlers.get_handlers(runner_name):
            error = handler.match(log_path)
            if error is not None:
                msg = handler.description.get()
                break

        if msg is not None:
            print(f"[ERROR] {msg}\n\n{error}\n")
            raise Exception(f"{msg}\n############# {label} - Failure #############")

    def get_label(self):
        raise NotImplementedError()

    def wait_runner(self, runner_id):
        if runner_id is None:
            raise Exception("Runner undefined")

        info = self.root().session().cmds.SubprocessManager.get_runner_info(runner_id)
        self.show_runner_info(info)
        while self.is_running(runner_id):
            time.sleep(1)
        self.show_message(f"[RUNNER] Runner {runner_id} finished")
        self.check_process_errors(info['log_path'], info['name'], self.get_label())


class TaskJobs(Jobs):

    @classmethod
    def job_type(cls):
        return TaskJob

    def create_job(self, job_type=None):
        name = '{}{:>05}'.format(self._get_job_prefix(), self._get_next_job_id())
        job = self.add(name, object_type=job_type)
        return job


class InitCompScene(GenericRunAction):
    ICON = ('icons.libreflow', 'afterfx')
    _shot = flow.Parent(3)
    _task = flow.Parent()
    _jsx_import_path = flow.Computed(cached=True)

    def __init__(self, parent, name):
        super(InitCompScene, self).__init__(parent, name)
        self._jsx_build_path = None

    def runner_name_and_tags(self):
        return 'AfterEffects', []

    def get_run_label(self):
        return "Create compositing scene"

    def target_file_extension(self):
        return 'aep'

    def needs_dialog(self):
        self._jsx_import_path.touch()
        msg = ""
        if self._jsx_import_path.get() is None:
            msg =  "<h2><font color=#D5000D>Rendering scene not yet exported</font></h2>"
            msg += "JSX import script not found in rendering task."
        self.message.set(msg)
        return True

    def get_buttons(self):
        if self._jsx_import_path.get() is None:
            return ['Cancel']

        return ['Build', 'Cancel']

    def extra_argv(self):
        return ['-m', '-r', self._jsx_build_path, '-noui']

    def compute_child_value(self, child_value):
        if child_value is self._jsx_import_path:
            self._jsx_import_path.set(self.get_jsx_import_script())

    def get_jsx_import_script(self):
        if not self._shot.tasks.has_mapped_name('rendering'):
            return None

        render_task = self._shot.tasks['rendering']
        if not render_task.files.has_file('compositing', 'jsx'):
            return None

        rev = render_task.files['compositing_jsx'].get_head_revision()
        if rev is None or rev.get_sync_status() != 'Available' or not os.path.isfile(rev.get_path()):
            return None

        return rev.get_path()

    def get_path_format(self, task_name, file_mapped_name):
        mng = self.root().project().get_task_manager()
        if not mng.default_tasks.has_mapped_name(task_name): # check default task
            # print(f'Scene Builder - no default task {task_name} -> use default template')
            return None

        dft_task = mng.default_tasks[task_name]
        if not dft_task.files.has_mapped_name(file_mapped_name): # check default file
            # print(f'Scene Builder - default task {task_name} has no default file {filename} -> use default template')
            return None

        dft_file = dft_task.files[file_mapped_name]
        return dft_file.path_format.get()

    def ensure_comp_scene(self):
        files = self._task.files
        name = 'compositing'
        ext = 'aep'
        file_name = "%s_%s" % (name, ext)
        path_format = self.get_path_format(
            self._task.name(), file_name)

        if files.has_file(name, ext):
            _file = files[file_name]
        else:
            _file = files.add_file(
                name=name,
                extension=ext,
                tracked=True,
                default_path_format=path_format,
            )
        _file.create_working_copy()
        rev = _file.publish(comment="Created with comp scene builder")
        return rev.get_path()

    def run(self, button):
        if button == 'Cancel':
            return
        
        d = get_contextual_dict(self, 'settings')
        if self._jsx_import_path.get() is None:
            print(f"[COMP SCENE BUILDER] {d['sequence']} {d['shot']} - Error: JSX script not found, building aborted.")
            return self.get_result(runner_id=None)

        print(f"[COMP SCENE BUILDER] {d['sequence']} {d['shot']} - building started...")
        scene_path = self.ensure_comp_scene().replace('\\', '\\\\')
        self._jsx_build_path = get_jsx_build_script(
            self._jsx_import_path.get(), scene_path)

        return super(InitCompScene, self).run(button)


class BuildRenderSceneJob(TaskJob):
    _shot = flow.Parent(4)

    def get_label(self):
        return 'BUILD RENDER SCENE'

    def _do_job(self):
        print(f"############# {self.get_label()} - Start #############")
        self.root().project().ensure_runners_loaded()
        build_render_scene = self._shot.tasks['rendering'].build_render_scene
        result = build_render_scene.run('Build')
        self.wait_runner(result['runner_id'])
        print(f"############# {self.get_label()} - End #############")


class RenderPassesJob(TaskJob):
    _tasks = flow.Parent(3)

    def get_render_scene(self):
        if not self._tasks.has_mapped_name('rendering'):
            return None, None

        task = self._tasks['rendering']
        if not task.files.has_file('rendering', 'blend'):
            return None, None

        _file = task.files['rendering_blend']
        rev = _file.get_head_revision()
        if rev is None or rev.get_sync_status() != 'Available' or not os.path.isfile(rev.get_path()):
            return None, None

        return _file, rev.name()

    def get_label(self):
        return 'RENDER PASSES'

    def _do_job(self):
        _file, rev_name = self.get_render_scene()
        if _file is None:
            raise Exception(f"Rendering scene not found")

        print(f"############# {self.get_label()} - Start #############")
        self.root().project().ensure_runners_loaded()
        render_playblast = _file.render_blender_playblast
        render_playblast.revision_name.set(rev_name)
        render_playblast.quality.set('Final')
        result = render_playblast.run('Render')
        self.wait_runner(result['runner_id'])
        print(f"############# {self.get_label()} - End #############")


class BuildCompSceneJob(TaskJob):
    _task = flow.Parent(2)

    def get_label(self):
        return 'BUILD COMPOSITING SCENE'

    def _do_job(self):
        # TODO: check missing files (compositing.jsx, passes)

        print(f"############# {self.get_label()} - Start #############")
        self.root().project().ensure_runners_loaded()
        init_comp_scene = self._task.init_comp_scene
        result = init_comp_scene.run('Create')
        self.wait_runner(result['runner_id'])
        print(f"############# {self.get_label()} - End #############")


class RenderImageSequenceJob(TaskJob):

    _task = flow.Parent(2)
    render_settings = flow.Param()
    output_module = flow.Param()

    def get_comp_scene(self):
        if not self._task.files.has_file('compositing', 'aep'):
            return None, None

        _file = self._task.files['compositing_aep']
        rev = _file.get_head_revision()
        if rev is None or rev.get_sync_status() != 'Available' or not os.path.isfile(rev.get_path()):
            return None, None

        return _file, rev.name()

    def get_label(self):
        return 'RENDER COMP SCENE'

    def _do_job(self):
        _file, rev_name = self.get_comp_scene()
        if _file is None:
            raise Exception(f"Compositing scene not found")

        print(f"############# {self.get_label()} - Start #############")
        self.root().project().ensure_runners_loaded()
        render_images = _file.render_image_sequence
        render_images.revision.set(rev_name)
        render_images.render_settings.set(self.render_settings.get())
        render_images.output_module.set(self.output_module.get())
        result = render_images.run('Render')
        self.wait_runner(result['runner_id'])
        print(f"############# {self.get_label()} - Success #############")


class ExportAudioJob(TaskJob):

    _task = flow.Parent(2)
    output_module = flow.Param()

    def get_comp_scene(self):
        if not self._task.files.has_file('compositing', 'aep'):
            return None, None

        _file = self._task.files['compositing_aep']
        rev = _file.get_head_revision()
        if rev is None or rev.get_sync_status() != 'Available' or not os.path.isfile(rev.get_path()):
            return None, None

        return _file, rev.name()

    def get_label(self):
        return 'EXPORT COMP AUDIO'

    def _do_job(self):
        _file, rev_name = self.get_comp_scene()
        if _file is None:
            raise Exception(f"Compositing scene not found")

        print(f"############# {self.get_label()} - Start #############")
        self.root().project().ensure_runners_loaded()
        export_audio = _file.export_ae_audio
        export_audio.revision.set(rev_name)
        export_audio.output_module.set(self.output_module.get())
        result = export_audio.run('Export')
        self.wait_runner(result['runner_id'])
        print(f"############# {self.get_label()} - End #############")


class MarkImageSequenceJob(TaskJob):

    _task = flow.Parent(2)
    output_module = flow.Param()

    def get_render_folder(self):
        if not self._task.files.has_folder('compositing_render'):
            return None, None

        folder = self._task.files['compositing_render']
        rev = folder.get_head_revision()
        if rev is None or rev.get_sync_status() != 'Available' or not os.path.isdir(rev.get_path()):
            return None, None

        return folder, rev.name()

    def get_label(self):
        return 'RENDER COMP MOVIE'

    def _do_job(self):
        folder, rev_name = self.get_render_folder()
        if folder is None:
            raise Exception(f"Compositing render folder not found")

        print(f"############# {self.get_label()} - Start #############")
        self.root().project().ensure_runners_loaded()
        mark_images = folder.mark_image_sequence
        mark_images.revision.set(rev_name)
        result = mark_images.run('Render')
        self.wait_runner(result['runner_id'])
        print(f"############# {self.get_label()} - End #############")


class BuildCompScene(flow.Action):
    ICON = ('icons.libreflow', 'afterfx')

    with flow.group('Advanced settings'):
        render_settings = flow.SessionParam(None, AERenderSettings)
        output_module = flow.SessionParam(None, AEOutputModule)

    _shot = flow.Parent(3)
    _task = flow.Parent()

    def needs_dialog(self):
        self.render_settings.revert_to_default()
        self.output_module.revert_to_default()
        return True

    def get_buttons(self):
        return ['Build', 'Cancel']

    def run(self, button):
        def submit_job(job, pool_name, label, user_name, paused):
            job.submit(pool_name, 100, label, \
                user_name, user_name, paused, False)

        if button == 'Cancel':
            return

        d = get_contextual_dict(self, 'settings')
        user_name = self.root().project().get_user_name()
        site = self.root().project().get_current_site()
        render_settings = (site.ae_render_settings_templates.get() or {}).get(
            self.render_settings.get())
        output_module = (site.ae_output_module_templates.get() or {}).get(
            self.output_module.get())
        audio_output_module = site.ae_output_module_audio.get()
        job_build_render = self._task.jobs.create_job(BuildRenderSceneJob)
        job_render_passes = self._task.jobs.create_job(RenderPassesJob)
        job_build_comp = self._task.jobs.create_job(BuildCompSceneJob)
        job_render_comp = self._task.jobs.create_job(RenderImageSequenceJob)
        job_render_comp.render_settings.set(render_settings)
        job_render_comp.output_module.set(output_module)
        job_export_comp_audio = self._task.jobs.create_job(ExportAudioJob)
        job_export_comp_audio.output_module.set(audio_output_module)
        job_render_comp_movie = self._task.jobs.create_job(MarkImageSequenceJob)
        LinkedJob.link_jobs(job_build_render, job_render_passes)
        LinkedJob.link_jobs(job_render_passes, job_build_comp)
        LinkedJob.link_jobs(job_build_comp, job_render_comp)
        LinkedJob.link_jobs(job_render_comp, job_export_comp_audio)
        LinkedJob.link_jobs(job_export_comp_audio, job_render_comp_movie)
        submit_job(job_build_render, 'compositing',
            f"BUILD SCENE {d['sequence']} {d['shot']} {d['task']} (1/6): build rendering scene",
            user_name, False)
        submit_job(job_render_passes, 'compositing',
            f"BUILD SCENE {d['sequence']} {d['shot']} {d['task']} (2/6): render passes",
            user_name, True)
        submit_job(job_build_comp, 'compositing',
            f"BUILD SCENE {d['sequence']} {d['shot']} {d['task']} (3/6): build compositing scene",
            user_name, True)
        submit_job(job_render_comp, 'compositing',
            f"BUILD SCENE {d['sequence']} {d['shot']} {d['task']} (4/6): render compositing scene",
            user_name, True)
        submit_job(job_export_comp_audio, 'compositing',
            f"BUILD SCENE {d['sequence']} {d['shot']} {d['task']} (5/6): export compositing scene audio",
            user_name, True)
        submit_job(job_render_comp_movie, 'compositing',
            f"BUILD SCENE {d['sequence']} {d['shot']} {d['task']} (6/6): render compositing movie",
            user_name, True)


def build_scene_action(parent):
    if isinstance(parent, Task) and parent.name() == "layout":
        r = flow.Child(BuildLayoutScene)
        r.name = 'build_layout_scene'
        r.index = None
        return r

    if isinstance(parent, Task) and parent.name() == "animblock":
        r = flow.Child(BuildBlockingScene)
        r.name = 'build_blocking_scene'
        r.index = None
        return r

    if isinstance(parent, Task) and parent.name() == "rendering":
        r = flow.Child(BuildRenderScene)
        r.name = 'build_render_scene'
        r.index = None
        return r

    if isinstance(parent, Task) and parent.name() == "comp":
        init_comp_scene = flow.Child(InitCompScene)
        init_comp_scene.name = 'init_comp_scene'
        init_comp_scene.index = None
        build_comp_scene = flow.Child(BuildCompScene)
        build_comp_scene.name = 'build_comp_scene'
        build_comp_scene.index = None
        jobs = flow.Child(TaskJobs)
        jobs.name = 'jobs'
        jobs.index = None
        return [
            init_comp_scene,
            build_comp_scene,
            jobs,
        ]

    if isinstance(parent, ProjectSettings):
        handlers = flow.Child(ErrorHandlers)
        handlers.name = 'runner_error_handlers'
        handlers.index = None
        return handlers

def install_extensions(session):
    return {
        "scene_builder": [
            build_scene_action
        ]
    }
