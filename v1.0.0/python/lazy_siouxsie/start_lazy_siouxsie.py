# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
import os
import sys
import threading
from maya import cmds
import glob
import re

# by importing QT from sgtk rather than directly, we ensure that
# the code will be compatible with both PySide and PyQt.
from sgtk.platform.qt import QtCore, QtGui
from .ui.lazy_siouxsie_ui import Ui_lazySiouxsie

def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    # in order to handle UIs seamlessly, each toolkit engine has methods for launching
    # different types of windows. By using these methods, your windows will be correctly
    # decorated and handled in a consistent fashion by the system. 
    
    # we pass the dialog class to this method and leave the actual construction
    # to be carried out by toolkit.
    app_instance.engine.show_dialog("Lazy Siouxsie Auto Turntables...", app_instance, LazySiouxsie)


class lazySiouzsieSignals(QtCore.QObject):
    progress = QtCore.Signal(int)


class lazySiouxsieEngine(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.signal = lazySiouzsieSignals()
        self._app = sgtk.platform.current_bundle()

        engine = self._app.engine
        self.sg = engine.sgtk
        self.context = engine.context
        self.project = self.context.project['name']
        self.project_id = self.context.project['id']
        self.entity = self.context.entity['type']
        self.task = self.context.task['name']
        self.entity_id = self.context.entity['id']
        self.file_path = None
        self.hdri_list = None
        self.custom_hdri = None

    def run(self, *args, **kwargs):
        self.build_turn_table()

    def build_turn_table(self):
        # List tasks
        next_file = self.find_turntable_task()
        if next_file:
            cmds.file(s=True)
            cmds.file(rn=next_file)
            cmds.file(s=True, type='mayaBinary')
            selected_hdri = self.get_hdri_files()

            lights = self.find_lights()

            file_to_return = self.file_path
            cmds.file(file_to_return, o=True)

    def find_lights(self):
        # Need to get the render engine and search for lights based on that.
        pass

    def get_hdri_files(self):
        hdri_files = []
        files_list = self.hdri_list
        if files_list:
            for hdri in files_list:
                hdri_files.append(self.hdri_path + '/' + hdri.text())
        if self.custom_hdri:
            hdri_files.append(self.custom_hdri)
        return hdri_files

    def find_turntable_task(self):
        filters = [
            ['entity', 'is', {'type': 'Asset', 'id': self.entity_id}]
        ]
        fields = ['content']
        tasks = self.sg.shotgun.find('Task', filters, fields)
        template = self.sg.templates['asset_work_area_maya']
        this_file = self.file_path
        path = os.path.dirname(this_file)
        # path = path.split('assets')[1]
        # path = 'assets' + path
        path = path.replace('\\', '/')
        settings = template.get_fields(path)
        turntable = None
        for task in tasks:
            content = task['content']
            task_id = task['id']
            if content == 'turntable.main':
                turntable = content
                turntable_id = task_id
                break
            else:
                turntable = None
                turntable_id = None
        tt_path = path.replace(settings['task_name'], 'turntable.main')
        print tt_path
        # template = self.sg.templates['maya_asset_work']
        version_pattern = r'(_v\d*|_V\d*)'
        if turntable:
            # Find latest turntable task
            if os.path.isdir(tt_path):
                files = glob.glob('%s/*[0-9]*' % tt_path)
                if files:
                    files.sort()
                    last_file = files[-1]
                    basename = os.path.basename(last_file)
                    version_string = re.search(version_pattern, basename)
                    last_version = version_string.group().lower()
                    version_number = int(last_version.strip('_v'))
                    next_version = version_number + 1
                    version_number = str(version_number)
                    next_version = str(next_version)
                    version = last_version.replace(version_number, next_version)
                    next_file = last_file.replace(last_version, version)
                else:
                    next_file = '%s/%s_turntable.main_v001.mb' % (tt_path, settings['Asset'])
            else:
                os.makedirs(tt_path)
                next_file = '%s/%s_turntable.main_v001.mb' % (tt_path, settings['Asset'])
        else:
            # Create Turntable Task
            filters = [
                ['code', 'is', 'Turntable']
            ]
            fields = ['id']
            step = self.sg.shotgun.find_one('Step', filters, fields)
            task_data = {
                'project': {'type': 'Project', 'id': self.project_id},
                'entity': {'type': 'Asset', 'id': self.entity_id},
                'content': 'turntable.main',
                'step': {'type': 'Step', 'id': step['id']},
            }
            new_task = self.sg.shotgun.create('Task', task_data)
            if not os.path.isdir(tt_path):
                os.makedirs(tt_path)
                next_file = '%s/%s_turntable.main_v001.mb' % (tt_path, settings['Asset'])
        return next_file


class LazySiouxsie(QtGui.QWidget):
    """
    Main application dialog window
    """
    
    def __init__(self, parent=None):
        """
        Constructor
        """
        # first, call the base class and let it do its thing.
        QtGui.QWidget.__init__(self, parent)
        self.siouxsie = lazySiouxsieEngine()
        
        # now load in the UI that was created in the UI designer
        self.ui = Ui_lazySiouxsie()
        self.ui.setupUi(self)
        
        # most of the useful accessors are available through the Application class instance
        # it is often handy to keep a reference to this. You can get it via the following method:
        self._app = sgtk.platform.current_bundle()

        engine = self._app.engine
        self.sg = engine.sgtk
        self.context = engine.context
        self.project = self.context.project['name']
        self.project_id = self.context.project['id']
        self.entity = self.context.entity['type']
        self.task = self.context.task['name']
        self.entity_id = self.context.entity['id']

        hdri_path = self._app.get_setting('hdri_path')
        if os.path.exists(hdri_path):
            self.hdri_path = hdri_path
            files = os.listdir(hdri_path)
            for f in files:
                filepath = os.path.join(hdri_path, f)
                if os.path.isfile(filepath):
                    if f.endswith('.hdr') or f.endswith('.exr'):
                        hdri = QtGui.QListWidgetItem(f)
                        self.ui.hdriList.addItem(hdri)
        file_to_send = cmds.file(q=True, sn=True)
        self.ui.file_path.setText(file_to_send)
        self.ui.file_path.setEnabled(False)
        self.ui.cancel_btn.clicked.connect(self.cancel)
        self.ui.spin_btn.clicked.connect(self.build_turn_table)
        self.ui.browse_btn.clicked.connect(self.browse)
        info = self.get_scene_details()
        self.ui.res_width.setText(info['width'])
        self.ui.res_height.setText(info['height'])

    def build_turn_table(self):
        if not self.siouxsie.isRunning():
            self.siouxsie.file_path = self.ui.file_path.text()
            self.siouxsie.hdri_list = self.ui.hdriList.selectedItems()
            self.siouxsie.custom_hdri = self.ui.custom_hdri.text()
            self.siouxsie.start()

    def cancel(self):
        self.close()

    def get_scene_details(self):
        filters = [
            ['name', 'is', self.project]
        ]
        fields = ['sg_renderers', 'sg_output_resolution', 'sg_frame_rate', 'sg_render_format', 'sg_pixel_aspect']
        projectInfo = self.sg.shotgun.find_one("Project", filters, fields)
        info = {}
        resolution = projectInfo['sg_output_resolution']
        info['width'] = resolution.split('x')[0]
        info['height'] = resolution.split('x')[1]
        info['frame_rate'] = projectInfo['sg_frame_rate']
        info['render_format'] = projectInfo['sg_render_format']['name']
        info['render_engine'] = projectInfo['sg_renderers'][0]['name']
        info['aspect_ratio'] = projectInfo['sg_pixel_aspect']
        return info

    def browse(self):
        finder = QtGui.QFileDialog.getOpenFileName(self, filter='HDRI (*.hdr *.exr)')
        if finder:
            self.ui.custom_hdri.setText(finder[0])



            # publish_data = {
            #     'project': {'type': 'Project', 'id': proj_id},
            #     'entity': {'type': 'Asset', 'id': asset_id},
            #     'task': {'type': 'Task', 'id': task_id},
            #     'name': 'design.main',
            #     'description': 'File was found in a watch folder and was auto-published.',
            #     'code': publish_name,
            #     'path_cache': publisher_path,
            #     'version_number': version,
            #     'published_file_type': published_file_type
            # }
            # new_publish = sg.create('PublishedFile', publish_data)
        
