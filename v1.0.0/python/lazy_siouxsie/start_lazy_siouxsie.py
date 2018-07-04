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
from time import sleep
import math

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

        self.turntable_task = self._app.get_setting('turntable_task')

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
                        self.ui.hdriList.setCurrentItem(hdri)
        file_to_send = cmds.file(q=True, sn=True)
        self.ui.file_path.setText(file_to_send)
        self.ui.file_path.setEnabled(False)
        self.ui.cancel_btn.clicked.connect(self.cancel)
        self.ui.spin_btn.clicked.connect(self.build_turn_table)
        self.ui.browse_btn.clicked.connect(self.browse)
        info = self.get_scene_details()
        self.ui.res_width.setText(info['width'])
        self.ui.res_height.setText(info['height'])
        self.ui.build_progress.setValue(0)

    def cancel(self):
        self.close()

    def build_turn_table(self):
        # List tasks
        next_file = self.find_turntable_task()
        if next_file:
            self.ui.build_progress.setValue(5)
            self.ui.status_label.setText('Saving working file...')
            cmds.file(s=True)
            self.ui.build_progress.setValue(7)
            self.ui.status_label.setText('Saving Turntable file...')
            print next_file
            cmds.file(rn=next_file)
            cmds.file(s=True, type='mayaBinary')
            self.ui.build_progress.setValue(8)
            self.ui.status_label.setText('Getting HDRI Selections...')
            selected_hdri = self.get_hdri_files()
            # Setup the camera bit
            self.ui.build_progress.setValue(10)
            self.ui.status_label.setText('Building the Turntable Camera...')
            start = int(self.ui.startFrame.text())
            end = int(self.ui.endFrame.text())
            camera = self.build_camera(start=start, end=end)
            # Get the rendering engine
            rendering_engine = self.ui.rendering_engine.currentIndex()
            # Based on engine, setup layers and create HDRI lights
            # If there are lights in the scene, setup a light layer
            # Animate the HDRIs
            # Setup the rendering setup
            # Send to the farm.

            self.ui.build_progress.setValue(97)
            self.ui.status_label.setText('Saving Turntable file...')
            cmds.file(s=True)
            self.ui.build_progress.setValue(98)
            self.ui.status_label.setText('Reopening the main file...')
            file_to_return = self.ui.file_path.text()
            cmds.file(file_to_return, o=True)
            self.ui.build_progress.setValue(100)
            self.ui.status_label.setText('Done!')
            sleep(3)
            self.cancel()

    def get_hdri_files(self):
        hdri_files = []
        files_list = self.ui.hdriList.selectedItems()
        if files_list:
            for hdri in files_list:
                hdri_files.append(self.hdri_path + '/' + hdri.text())
        if self.ui.custom_hdri.text():
            hdri_files.append(self.ui.custom_hdri.text())
        return hdri_files

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
        self.ui.build_progress.setValue(1)
        self.ui.status_label.setText('Getting Shotgun Tasks...')
        template = self.sg.templates['asset_work_area_maya']
        this_file = self.ui.file_path.text()
        path = os.path.dirname(this_file)
        # path = path.split('assets')[1]
        # path = 'assets' + path
        path = path.replace('\\', '/')
        settings = template.get_fields(path)
        for task in tasks:
            content = task['content']
            task_id = task['id']
            if content == self.turntable_task:
                turntable = content
                turntable_id = task_id
                break
            else:
                turntable = None
                turntable_id = None
        tt_path = path.replace(settings['task_name'], self.turntable_task)
        self.ui.build_progress.setValue(3)
        self.ui.status_label.setText('Turntable path: %s' % tt_path)
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
                    next_file = '%s/%s_%s_v001.mb' % (tt_path, settings['Asset'], self.turntable_task)
            else:
                os.makedirs(tt_path)
                next_file = '%s/%s_%s_v001.mb' % (tt_path, settings['Asset'], self.turntable_task)
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
                'content': self.turntable_task,
                'step': {'type': 'Step', 'id': step['id']},
            }
            new_task = self.sg.shotgun.create('Task', task_data)
            if not os.path.isdir(tt_path):
                os.makedirs(tt_path)
                next_file = '%s/%s_%s_v001.mb' % (tt_path, settings['Asset'], self.turntable_task)
        self.ui.build_progress.setValue(4)
        self.ui.status_label.setText('New Filename: %s' % next_file)
        return next_file

    def build_camera(self, start=1, end=120):
        # Select and group the set
        self.ui.build_progress.setValue(11)
        self.ui.status_label.setText('Selecting scene geometry...')
        geo = cmds.ls(type=['mesh', 'nurbsSurface'])
        cmds.select(geo, r=True)
        z = 30
        while z < 100:
            cmds.pickWalk(d='up')
            z += 1
        self.ui.build_progress.setValue(12)
        self.ui.status_label.setText('Grouping the geometry...')
        cmds.group(n='Set_prep')
        # Get the set/scene size from the bounding box
        cmds.select('Set_prep')
        self.ui.build_progress.setValue(13)
        self.ui.status_label.setText('Getting scene center point...')
        scene_bb = cmds.xform(q=True, bb=True)
        # Find the center from the bounding box
        x_center = scene_bb[3] - ((scene_bb[3] - scene_bb[0]) / 2)
        y_center = scene_bb[4] - ((scene_bb[4] - scene_bb[1]) / 2)
        z_center = scene_bb[5] - ((scene_bb[5] - scene_bb[2]) / 2)
        bb_center = [x_center, y_center, z_center]
        # calculate a new height for the camera based on the bounding box
        cam_height = scene_bb[4] - scene_bb[1]
        # Create a new camera and fit it to the current view
        self.ui.build_progress.setValue(14)
        self.ui.status_label.setText('Creating camera...')
        cam = cmds.camera(n='turn_table_cam')
        cmds.lookThru(cam)
        cmds.viewFit()
        self.ui.build_progress.setValue(15)
        self.ui.status_label.setText('Beginning camera position calculations...')
        # Get the position of the new camera after placement
        cam_pos = cmds.xform(q=True, ws=True, t=True)
        # Separate out the mins and maxs of the bounding box for triangulation
        self.ui.build_progress.setValue(16)
        x_min = scene_bb[0]
        x_max = scene_bb[3]
        y_min = scene_bb[1]
        y_max = scene_bb[4]
        z_min = scene_bb[2]
        z_max = scene_bb[5]
        # Get the cube root hypotenuse of the bounding box to calculate the overall scene's widest distance
        self.ui.build_progress.setValue(17)
        cube_diff = math.pow((x_max - x_min), 3) + math.pow((y_max - y_min), 3) + math.pow((z_max - z_min), 3)
        max_hypotenuse = cube_diff ** (1. / 3.)
        # Cut the width in half to create a 90 degree angle
        self.ui.build_progress.setValue(18)
        half_width = max_hypotenuse / 2
        # Get the horizontal aperture. Only the inch aperture is accessible, so mm aperture and field of view must be calculated from that
        horizontalApertureInch = cmds.getAttr('%s.horizontalFilmAperture' % cam[1])
        # convert to mm
        horizontalAperture_mm = 2.54 * horizontalApertureInch * 10
        # Get focal length
        focalLength = cmds.getAttr('%s.focalLength' % cam[1])
        # Calculate FOV from horizontal aperture and focal length
        self.ui.build_progress.setValue(19)
        fov = math.degrees(2 * math.atan(horizontalAperture_mm / (focalLength * 2)))
        # Cut the FOV in half to get angle of right angle.
        half_angle = fov / 2
        # Calculate the distance for the camera
        self.ui.build_progress.setValue(20)
        angle_tan = math.tan(half_angle)
        distance = cam_pos[2] - (half_width / angle_tan)
        # Set the new camera distance and height
        self.ui.build_progress.setValue(21)
        self.ui.status_label.setText('Adjusting camera position...')
        cmds.setAttr('%s.ty' % cam[0], cam_height)
        cmds.setAttr('%s.tz' % cam[0], distance)
        # Get the new camera position
        cam_pos = cmds.xform(q=True, t=True, ws=True)
        # Calculate the decension angle from the center of the scene to the new camera position
        self.ui.build_progress.setValue(22)
        self.ui.status_label.setText('Adjusting camera angle...')
        cam_height = cam_pos[1] - bb_center[1]
        cam_dist = cam_pos[2] - bb_center[2]
        cam_angle = -1 * (math.degrees(cam_height / cam_dist))
        # Set the declination angle
        cmds.setAttr('%s.rx' % cam[0], cam_angle)
        # Group the camera, center the pivot, and animate the rotation

        self.ui.build_progress.setValue(23)
        self.ui.status_label.setText('Animating the camera...')
        cmds.group(n='turn_table_rotate')
        cmds.xform(piv=[x_center, y_center, z_center])
        cmds.setKeyframe('turn_table_rotate.ry', v=0.0, ott='linear', t=start)
        cmds.setKeyframe('turn_table_rotate.ry', v=360.0, itt='linear', t=end)
        return cam


