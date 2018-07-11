# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
GOALS:
1. Connect all of the other UI elements, Frame size, rate, aspect ratio
2. Create the Gray and Mirror Balls
3. Setup the quality and render settings
4. Setup the Deadline script
5. Get the lights layer working
"""

import sgtk
import os
import sys
import threading
import maya.app.renderSetup.model.override as override
import maya.app.renderSetup.model.selector as selector
import maya.app.renderSetup.model.collection as collection
import maya.app.renderSetup.model.renderLayer as renderLayer
import maya.app.renderSetup.model.renderSetup as renderSetup
import maya.app.renderSetup.views.overrideUtils as utils
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

        filters = [
            ['id', 'is', self.project_id]
        ]
        fields = [
            'sg_pixel_aspect',
            'sg_output_resolution',
            'sg_renderers'
        ]
        sg_settings = self.sg.shotgun.find_one('Project', filters, fields)

        sg_resolution = sg_settings['sg_output_resolution']
        split_res = sg_resolution.split('x')
        resolution_width = split_res[0]
        resolution_height = split_res[1]
        pixel_aspect = str(sg_settings['sg_pixel_aspect'])
        renderers = sg_settings['sg_renderers'][0]['name']

        self.ui.res_width.setText(resolution_width)
        self.ui.res_height.setText(resolution_height)
        self.ui.pixel_aspect.setText(pixel_aspect)
        self.ui.rendering_engine.setCurrentText(renderers)

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
        self.ui.total_frames.setEnabled(False)
        self.ui.startFrame.valueChanged.connect(self.set_frames)
        self.ui.endFrame.valueChanged.connect(self.set_frames)

    def set_frames(self):
        start = self.ui.startFrame.value()
        end = self.ui.endFrame.value()
        dif = (end - start) + 1
        total_frames = dif * 2
        self.ui.total_frames.setText(str(total_frames))

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
            cmds.file(rn=next_file)
            cmds.file(s=True, type='mayaBinary')
            self.ui.build_progress.setValue(8)
            self.ui.status_label.setText('Getting HDRI Selections...')
            selected_hdri = self.get_hdri_files()
            # Setup the camera bit
            self.ui.build_progress.setValue(10)
            self.ui.status_label.setText('Building the Turntable Camera...')
            start = self.ui.startFrame.value()
            end = self.ui.endFrame.value()
            camera_data = self.build_camera(start=start, end=end)
            camera = camera_data[0]
            center = camera_data[1]
            bb = camera_data[2]
            scene_max_width = camera_data[3]
            x_min = bb[0]
            y_min = bb[1]
            z_min = bb[2]
            x_max = bb[3]
            y_max = bb[4]
            z_max = bb[5]

            self.ui.build_progress.setValue(24)
            self.ui.status_label.setText('Set frame ranges...')
            total_frames = int(self.ui.total_frames.text())
            add_frames = total_frames/2
            extended_end = end + add_frames
            cmds.playbackOptions(min=start, max=extended_end)
            # Get the rendering engine
            self.ui.build_progress.setValue(25)
            self.ui.status_label.setText('Get the rendering engine...')
            rendering_engine = self.ui.rendering_engine.currentText()
            lights = self.ui.scene_lights.isChecked()

            # This will need some major renumbering
            self.ui.build_progress.setValue(33)
            self.ui.status_label.setText('Get scene lighting requirements...')
            use_scene_lighting = self.ui.scene_lights.isChecked()
            if use_scene_lighting:
                self.ui.build_progress.setValue(35)
                self.ui.status_label.setText('Get Scene Lights...')
                get_scene_lights = self.get_scene_lights(renderer=rendering_engine)
            else:
                self.ui.build_progress.setValue(35)
                self.ui.status_label.setText('Ignoring scene lights...')
                get_scene_lights = None

            self.ui.build_progress.setValue(26)
            self.ui.status_label.setText('Build HDRI dome...')
            hdri_dome = self.build_hdri_dome(renderer=rendering_engine, lights=lights, hdri_list=selected_hdri,
                                             center=center)
            dome = hdri_dome['dome']
            file_node = hdri_dome['file']
            light_trans = hdri_dome['translation']

            self.ui.build_progress.setValue(30)
            self.ui.status_label.setText('Animating the HDRI dome...')
            self.animate_dome(trans=light_trans, start=end, end=extended_end)

            self.ui.build_progress.setValue(31)
            self.ui.status_label.setText('Check groundplane setting...')
            ground = self.ui.ground_plane.isChecked()
            ground_plane = None
            if ground:
                self.ui.build_progress.setValue(31)
                self.ui.status_label.setText('Building Ground Plane...')
                radius = 10 * scene_max_width
                if cmds.about(q=True, v=True) < '2018':
                    ground_plane = cmds.polyPlane(h=radius, w=radius, ax=[0, 1, 0], ch=True, cuv=2,
                                                  n='_turntable_ground_plane', sx=10, sy=20)
                    self.texture_ground(ground=ground_plane, renderer=rendering_engine)
                else:
                    cmds.polyDisc(s=4, sm=4, sd=3, r=radius)
                    cmds.rename('_turntable_ground_plane')
                    ground_plane = cmds.ls(sl=True)[0]
                    self.texture_ground(ground=ground_plane, renderer=rendering_engine)
                self.ui.build_progress.setValue(32)
                self.ui.status_label.setText('Set the plane Position...')
                cmds.select(ground_plane, r=True)
                cmds.setAttr('%s.tx' % ground_plane, center[0])
                cmds.setAttr('%s.ty' % ground_plane, y_min)
                cmds.setAttr('%s.tz' % ground_plane, center[2])

            get_spheres = self.ui.chrome_balls.isChecked()
            spheres = []
            if get_spheres:
                base_max_width = math.sqrt((math.pow((x_max - x_min), 2)) + (math.pow((y_max - y_min), 2)))
                sphere_radius = ((y_max - y_min)/2) * 0.25
                chrome_ball = cmds.polySphere(r=sphere_radius, n='_turntable_chrome_ball')
                gray_ball = cmds.polySphere(r=sphere_radius, n='_turntable_gray_ball')

                # positioning of the chrome balls
                chrome_x_point = center[0] + ((base_max_width / 2) * .85)
                gray_x_point = chrome_x_point + (sphere_radius * 2.2)
                sphere_ground = y_min + sphere_radius
                cmds.setAttr('%s.tx' % chrome_ball[0], chrome_x_point)
                cmds.setAttr('%s.ty' % chrome_ball[0], sphere_ground)
                cmds.setAttr('%s.tz' % chrome_ball[0], center[2])
                cmds.setAttr('%s.tx' % gray_ball[0], gray_x_point)
                cmds.setAttr('%s.ty' % gray_ball[0], sphere_ground)
                cmds.setAttr('%s.tz' % gray_ball[0], center[2])
                spheres.append(chrome_ball)
                spheres.append(gray_ball)
                materials = self.texture_chrome_balls(spheres=spheres, renderer=rendering_engine)
                print materials

            self.ui.build_progress.setValue(50)
            self.ui.status_label.setText('Begin Layers Setup...')
            self.setup_render_layers(dome=dome, file_node=file_node, ground=ground_plane, light_trans=light_trans,
                                     hdri_list=selected_hdri, lights=get_scene_lights, balls=spheres)

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

    def texture_ground(self, ground=None, renderer=None):
        if ground:
            print ground
            if renderer == 'arnold':
                material = cmds.shadingNode('aiShadowMatte', asShader=True, n='_turntable_ground_mat')
                cmds.select(ground, r=True)
                cmds.hyperShade(a=material)

    def texture_chrome_balls(self, spheres=None, renderer=None):
        materials = {}
        if spheres:
            chrome_transform = spheres[0][0]
            chrome_shape = spheres[0][1]
            gray_transform = spheres[1][0]
            gray_shape = spheres[1][1]
            if renderer == 'arnold':
                gray_surface = cmds.shadingNode('aiStandardSurface', asShader=True, n='_turntable_gray_mat')
                chrome_surface = cmds.shadingNode('aiStandardSurface', asShader=True, n='_turntable_chrome_mat')
                cmds.select(chrome_transform, r=True)
                cmds.hyperShade(a=chrome_surface)
                cmds.select(gray_transform, r=True)
                cmds.hyperShade(a=gray_surface)

                cmds.setAttr('%s.metalness' % chrome_surface, 1)
                cmds.setAttr('%s.base' % chrome_surface, 1)
                cmds.setAttr('%s.baseColor' % chrome_surface, 1, 1, 1, type='double3')
                cmds.setAttr('%s.specular' % chrome_surface, 0)
                cmds.setAttr('%s.specularAnisotropy' % chrome_surface, 0.5)

                cmds.setAttr('%s.base' % gray_surface, 1)
                cmds.setAttr('%s.baseColor' % gray_surface, 0.5, 0.5, 0.5, type='double3')
                cmds.setAttr('%s.specularColor' % gray_surface, 0.5, 0.5, 0.5, type='double3')
                cmds.setAttr('%s.specular' % gray_surface, 1)
                cmds.setAttr('%s.specularRoughness' % gray_surface, 0.65)

            elif renderer == 'vray':
                gray_surface = cmds.shadingNode('VRayMtl', asShader=True, n='_turntable_gray_mat')
                chrome_surface = cmds.shadingNode('VRayMtl', asShader=True, n='_turntable_chrome_mat')
                cmds.select(chrome_transform, r=True)
                cmds.hyperShade(a=chrome_surface)
                cmds.select(gray_transform, r=True)
                cmds.hyperShade(a=gray_surface)

                cmds.setAttr('%s.useFresnel' % chrome_surface, 0)
                cmds.setAttr('%s.reflectionColor' % chrome_surface, 1, 1, 1, type='double3')
                cmds.setAttr('%s.diffuseColorAmount' % chrome_surface, 0)
                cmds.setAttr('%s.color' % chrome_surface, 1, 1, 1, type='double3')

                cmds.setAttr('%s.color' % gray_surface, 0.5, 0.5, 0.5, type='double3')
                cmds.setAttr('%s.reflectionColor' % gray_surface, 0.5, 0.5, 0.5, type='double3')
                cmds.setAttr('%s.hilightGlossinessLock' % gray_surface, 0)
                cmds.setAttr('%s.reflectionGlossiness' % gray_surface, 0)
                cmds.setAttr('%s.hilightGlossiness' % gray_surface, 0.35)
            elif renderer == 'renderman':
                pass
            elif renderer == 'redshift':
                pass
            else:
                gray_surface = cmds.shadingNode('blinn', asShader=True, n='_turntable_gray_mat')
                chrome_surface = cmds.shadingNode('blinn', asShader=True, n='_turntable_chrome_mat')
                cmds.select(chrome_transform, r=True)
                cmds.hyperShade(a=chrome_surface)
                cmds.select(gray_transform, r=True)
                cmds.hyperShade(a=gray_surface)

            materials['gray_shader'] = gray_surface
            materials['chrome_shader'] = chrome_surface

        return materials

        # setAttr
        # "_turntable_gray_mat.specularRoughness"
        # 0.3;
        # setAttr
        # "_turntable_gray_mat.specularRoughness"
        # 0.65;
        # setAttr
        # "defaultArnoldRenderOptions.GIDiffuseSamples"
        # 6;
        # setAttr
        # "defaultArnoldRenderOptions.GISpecularSamples"
        # 4;
        # setAttr
        # "defaultArnoldRenderOptions.GITransmissionSamples"
        # 4;
        # setAttr
        # "defaultArnoldRenderOptions.GISssSamples"
        # 4;
        # setAttr
        # "defaultArnoldRenderOptions.GIVolumeSamples"
        # 4;
        # setAttr
        # "defaultArnoldRenderOptions.AASamples"
        # 12;
        # setAttr
        # "defaultArnoldRenderOptions.AASamples"
        # 6;

    def build_hdri_dome(self, renderer=None, lights=None, hdri_list=None, center=None):
        hdri = {}
        if renderer == 'arnold':
            self.ui.build_progress.setValue(27)
            self.ui.status_label.setText('Create Arnold SkyDome...')
            light = cmds.createNode('aiSkyDomeLight')
            self.ui.build_progress.setValue(28)
            self.ui.status_label.setText('Get parent translation...')
            cmds.pickWalk(d='up')
            cmds.rename('_HDRI_light')
            light_trans = cmds.ls(sl=True)[0]
            self.ui.build_progress.setValue(29)
            self.ui.status_label.setText('Connect Light to file...')
            cmds.connectAttr('%s.instObjGroups' % light_trans, 'defaultLightSet.dagSetMembers', na=True)
            file_node = cmds.createNode('file')
            # The following will need to be setup by the list of HDRIs, BUT I need to get the file/light name returned.
            # cmds.setAttr('%s.fileTextureName' % file_node,
            #              r'\\elephant\SleepDeprived\Assets\Images\HDRI\CGSkies_0094_free.hdr', type='string')
            cmds.connectAttr('%s.outColor' % file_node, '%s.color' % light, f=True)
            hdri['dome'] = light
            hdri['file'] = file_node
            hdri['translation'] = light_trans
        elif renderer == 'vray':
            self.ui.build_progress.setValue(27)
            self.ui.status_label.setText('Create VRay Dome Light...')
            light = cmds.createNode('VRayLightDomeShape')
            self.ui.build_progress.setValue(28)
            self.ui.status_label.setText('Get parent translation...')
            cmds.pickWalk(d='up')
            cmds.rename('_HDRI_light')
            light_trans = cmds.ls(sl=True)[0]
            self.ui.build_progress.setValue(29)
            self.ui.status_label.setText('Connect Light to file...')
            cmds.setAttr('%s.useDomeTex' % light, 1)
            file_node = cmds.createNode('file')
            cmds.connectAttr('%s.outColor' % file_node, '%s.domeTex' % light, r=True)
            hdri['dome'] = light
            hdri['file'] = file_node
            hdri['translation'] = light_trans
        elif renderer == 'redshift':
            # Figure out RedShift code
            pass
        elif renderer == 'renderman':
            # Figure out RedShift code
            pass
        elif renderer == 'mayasoftware':
            pass
        cmds.select(light_trans, r=True)
        cmds.xform(t=center, ws=True)
        return hdri

    def get_hdri_files(self):
        hdri_files = []
        files_list = self.ui.hdriList.selectedItems()
        if files_list:
            for hdri in files_list:
                hdri_files.append(self.hdri_path + '/' + hdri.text())
        if self.ui.custom_hdri.text():
            hdri_files.append(self.ui.custom_hdri.text())
        return hdri_files

    def setup_render_layers(self, dome=None, file_node=None, ground=None, light_trans=None, hdri_list=None,
                            lights=[], balls=[]):
        rs = renderSetup.instance()
        # lights = list(lights)

        if lights:
            # TODO: Eventually, I need to get this working. For now it is disabled, but will hide all the lights.

            # render_layer = rs.createRenderLayer('Artist_Lights')
            # collection_set = render_layer.createCollection('geo')
            # collection_set.getSelector().setPattern('_Turntable_Set_Prep, %s' % ground)
            # light_collection = render_layer.createCollection('artist_lights')
            # light_list = ''
            # for light in lights:
            #     light_list += '%s, ' % light
            # light_collection.getSelector().setPattern(light_list)
            # light_collection.setSelectorType('Lights')

            # light_collection.getSelector().set
            # light_collection.
            for light in lights:
                cmds.select(light, r=True)
                cmds.hide()
            # rs.switchToLayer(render_layer)
            # for light in lights:
            # utils.createAbsoluteOverride(light, 'visibility')
            #
            # cmds.setAttr('visibility.attrValue', 1)
            # cmds.select(light, r=True)

        chrome_balls = ''
        if balls:
            for ball in balls:
                chrome_balls = '%s, %s' % (chrome_balls, ball[0])
        if hdri_list:
            for hdri in hdri_list:
                # Get the basic filename for the render layer name
                basename = os.path.basename(hdri)
                base = os.path.splitext(basename)[0]
                render_layer = rs.createRenderLayer(base)
                collection_set = render_layer.createCollection('Scene_%s' % base)
                collection_set.getSelector().setPattern('_Turntable_Set_Prep, %s, %s' % (chrome_balls, ground))
                rs.switchToLayer(render_layer)
                utils.createAbsoluteOverride(file_node, 'fileTextureName')
                cmds.setAttr('%s.fileTextureName' % file_node, hdri, type='string')
        # rs.switchToLayer('defaultRenderLayer')

    def get_scene_lights(self, renderer=None):
        lights = []
        if renderer == 'arnold':
            self.ui.build_progress.setValue(36)
            self.ui.status_label.setText('Getting Arnold Lights...')
            light_types = ['aiAreaLight', 'aiSkyDomeLight', 'aiMeshLight', 'aiPhotometricLight', 'aiLightPortal',
                           'aiPhysicalSky']
            for light in light_types:
                type_list = cmds.ls(type=light)
                for t in type_list:
                    lights.append(t)
        elif renderer == 'vray':
            # Figure out the vray code...
            pass
        elif renderer == 'redshift':
            # Figure out RedShift code
            pass
        elif renderer == 'renderman':
            # Figure out RedShift code
            pass
        elif renderer == 'mayasoftware':
            pass

        self.ui.build_progress.setValue(39)
        self.ui.status_label.setText('getting Maya Lights...')
        for light in cmds.ls(lt=True):
            lights.append(light)
        return lights

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
                    version_number = last_version.strip('_v')
                    version_count = len(version_number)
                    version_number = int(version_number)
                    next_version = version_number + 1
                    version_number = str('{n:0{l}d}'.format(n=version_number, l=version_count))
                    next_version_number = str('{n:0{l}d}'.format(n=next_version, l=version_count))
                    version = last_version.replace(version_number, next_version_number)
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
        cmds.group(n='_Turntable_Set_Prep')
        # Get the set/scene size from the bounding box
        cmds.select('_Turntable_Set_Prep')
        self.ui.build_progress.setValue(13)
        self.ui.status_label.setText('Getting scene center point...')
        scene_bb = cmds.xform(q=True, bb=True)
        # Find the center from the bounding box
        x_center = scene_bb[3] - ((scene_bb[3] - scene_bb[0]) / 2)
        y_center = scene_bb[4] - ((scene_bb[4] - scene_bb[1]) / 2)
        z_center = scene_bb[5] - ((scene_bb[5] - scene_bb[2]) / 2)
        self.ui.build_progress.setValue(14)
        self.ui.status_label.setText('Animating the Set...')
        cmds.select('_Turntable_Set_Prep', r=True)
        bb_center = [x_center, y_center, z_center]
        cmds.xform(piv=[x_center, y_center, z_center])
        cmds.setKeyframe('_Turntable_Set_Prep.ry', v=-25, ott='linear', t=start)
        cmds.setKeyframe('_Turntable_Set_Prep.ry', v=-385.0, itt='linear', t=end)
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
        res_width = float(self.ui.res_width.text())
        res_height = float(self.ui.res_height.text())
        aspect_ratio = res_width / res_height
        height = (y_max - y_min)
        width = (x_max - x_min)
        depth = (z_max - z_min)
        if height > width and height > depth:
            max_hypotenuse *= aspect_ratio
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
        new_cam_pos = cmds.xform(q=True, t=True, ws=True)
        # Calculate the decension angle from the center of the scene to the new camera position
        self.ui.build_progress.setValue(22)
        self.ui.status_label.setText('Adjusting camera angle...')
        cam_height = new_cam_pos[1] - bb_center[1]
        cam_dist = new_cam_pos[2] - bb_center[2]
        cam_angle = -1 * (math.degrees(math.atan(cam_height / cam_dist)))
        # Set the declination angle
        cmds.setAttr('%s.rx' % cam[0], cam_angle)
        # Group the camera, center the pivot, and animate the rotation

        self.ui.build_progress.setValue(23)
        self.ui.status_label.setText('Animating the camera...')
        cmds.group(n='_turntable_cam')
        return [cam, bb_center, scene_bb, max_hypotenuse]

    def animate_dome(self, trans=None, start=None, end=None):
        if trans:
            cmds.setKeyframe('%s.ry' % trans, v=25, ott='linear', t=start)
            cmds.setKeyframe('%s.ry' % trans, v=-385.0, itt='linear', t=end)

