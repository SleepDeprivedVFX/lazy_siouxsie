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
    


class LazySiouxsie(QtGui.QWidget):
    """
    Main application dialog window
    """
    
    def __init__(self):
        """
        Constructor
        """
        # first, call the base class and let it do its thing.
        QtGui.QWidget.__init__(self)
        
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


    def cancel(self):
        self.close()

    def build_turn_table(self):
        # List tasks
        task = self.find_turntable_task()

    def browse(self):
        finder = QtGui.QFileDialog.getOpenFileName(self, filter='HDRI (*.hdr *.exr)')
        if finder:
            self.ui.custom_hdri.setText(finder[0])

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

    def find_turntable_task(self):
        filters = [
            ['entity', 'is', {'type': 'Asset', 'id': self.entity_id}]
        ]
        fields = ['content']
        tasks = self.sg.shotgun.find('Task', filters, fields)
        template = self.sg.templates['asset_work_area_maya']
        print template
        this_file = self.ui.file_path.text()
        path = os.path.dirname(this_file)
        # path = path.split('assets')[1]
        # path = 'assets' + path
        path = path.replace('\\', '/')
        print path
        settings = template.get_fields(path)
        print settings
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
        template = self.sg.templates['maya_asset_work']
        if turntable:
            # Find latest turntable task
            if os.path.isdir(tt_path):
                files = os.listdir(tt_path)
                if files:
                    files.sort()
                    for f in files:
                        check_file = os.path.join(tt_path, f)
                        if os.path.isfile(check_file):
                            print check_file
            else:
                os.makedirs(tt_path)
        else:
            # Create Turntable Task
            filters = [
                ['code', 'is', 'Turntable']
            ]
            fields = ['id']
            step = self.sg.shotgun.find_one('Step', filters, fields)
            print step
            task_data = {
                'project': {'type': 'Project', 'id': self.project_id},
                'entity': {'type': 'Asset', 'id': self.entity_id},
                'content': 'turntable.main',
                'step': {'type': 'Step', 'id': step['id']},
            }
            new_task = self.sg.shotgun.create('Task', task_data)
            if not os.path.isdir(tt_path):
                os.makedirs(tt_path)

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
        
