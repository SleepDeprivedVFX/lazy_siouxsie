# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\sleep\OneDrive\Documents\shotgun\mastertemplate\install\manual\tk-lazy_siouxsie\v1.0.0\python\lazy_siouxsie\ui\lazy_siouxsie_ui.ui'
#
# Created: Sat Jul 07 00:58:25 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from sgtk.platform.qt import QtCore, QtGui

class Ui_lazySiouxsie(object):
    def setupUi(self, lazySiouxsie):
        lazySiouxsie.setObjectName("lazySiouxsie")
        lazySiouxsie.resize(557, 708)
        self.verticalLayout_2 = QtGui.QVBoxLayout(lazySiouxsie)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title = QtGui.QLabel(lazySiouxsie)
        self.title.setStyleSheet("font: 75 italic 12pt \"MS Shell Dlg 2\";")
        self.title.setObjectName("title")
        self.verticalLayout_2.addWidget(self.title)
        self.subTitle = QtGui.QLabel(lazySiouxsie)
        self.subTitle.setStyleSheet("font: 75 italic 10pt \"MS Shell Dlg 2\";")
        self.subTitle.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.subTitle.setObjectName("subTitle")
        self.verticalLayout_2.addWidget(self.subTitle)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.file_label = QtGui.QLabel(lazySiouxsie)
        self.file_label.setObjectName("file_label")
        self.horizontalLayout_5.addWidget(self.file_label)
        self.file_path = QtGui.QLineEdit(lazySiouxsie)
        self.file_path.setObjectName("file_path")
        self.horizontalLayout_5.addWidget(self.file_path)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hdri_label = QtGui.QLabel(lazySiouxsie)
        self.hdri_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.hdri_label.setObjectName("hdri_label")
        self.horizontalLayout.addWidget(self.hdri_label)
        self.hdriList = QtGui.QListWidget(lazySiouxsie)
        self.hdriList.setAlternatingRowColors(True)
        self.hdriList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.hdriList.setObjectName("hdriList")
        self.horizontalLayout.addWidget(self.hdriList)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.custom = QtGui.QLabel(lazySiouxsie)
        self.custom.setObjectName("custom")
        self.horizontalLayout_3.addWidget(self.custom)
        self.custom_hdri = QtGui.QLineEdit(lazySiouxsie)
        self.custom_hdri.setObjectName("custom_hdri")
        self.horizontalLayout_3.addWidget(self.custom_hdri)
        self.browse_btn = QtGui.QPushButton(lazySiouxsie)
        self.browse_btn.setObjectName("browse_btn")
        self.horizontalLayout_3.addWidget(self.browse_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.frame_statement = QtGui.QLabel(lazySiouxsie)
        self.frame_statement.setWordWrap(True)
        self.frame_statement.setObjectName("frame_statement")
        self.verticalLayout_2.addWidget(self.frame_statement)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.startLabel = QtGui.QLabel(lazySiouxsie)
        self.startLabel.setObjectName("startLabel")
        self.horizontalLayout_2.addWidget(self.startLabel)
        self.startFrame = QtGui.QSpinBox(lazySiouxsie)
        self.startFrame.setMaximum(50000)
        self.startFrame.setProperty("value", 1001)
        self.startFrame.setObjectName("startFrame")
        self.horizontalLayout_2.addWidget(self.startFrame)
        self.endLabel = QtGui.QLabel(lazySiouxsie)
        self.endLabel.setObjectName("endLabel")
        self.horizontalLayout_2.addWidget(self.endLabel)
        self.endFrame = QtGui.QSpinBox(lazySiouxsie)
        self.endFrame.setMaximum(50000)
        self.endFrame.setProperty("value", 1120)
        self.endFrame.setObjectName("endFrame")
        self.horizontalLayout_2.addWidget(self.endFrame)
        self.totalFrameLabel = QtGui.QLabel(lazySiouxsie)
        self.totalFrameLabel.setObjectName("totalFrameLabel")
        self.horizontalLayout_2.addWidget(self.totalFrameLabel)
        self.total_frames = QtGui.QLineEdit(lazySiouxsie)
        self.total_frames.setMaximumSize(QtCore.QSize(75, 16777215))
        self.total_frames.setReadOnly(False)
        self.total_frames.setObjectName("total_frames")
        self.horizontalLayout_2.addWidget(self.total_frames)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.resolution_label = QtGui.QLabel(lazySiouxsie)
        self.resolution_label.setObjectName("resolution_label")
        self.horizontalLayout_6.addWidget(self.resolution_label)
        self.res_width = QtGui.QLineEdit(lazySiouxsie)
        self.res_width.setMaximumSize(QtCore.QSize(120, 16777215))
        self.res_width.setMaxLength(8)
        self.res_width.setObjectName("res_width")
        self.horizontalLayout_6.addWidget(self.res_width)
        self.x_label = QtGui.QLabel(lazySiouxsie)
        self.x_label.setObjectName("x_label")
        self.horizontalLayout_6.addWidget(self.x_label)
        self.res_height = QtGui.QLineEdit(lazySiouxsie)
        self.res_height.setMaximumSize(QtCore.QSize(120, 16777215))
        self.res_height.setMaxLength(8)
        self.res_height.setObjectName("res_height")
        self.horizontalLayout_6.addWidget(self.res_height)
        self.res_scale = QtGui.QComboBox(lazySiouxsie)
        self.res_scale.setObjectName("res_scale")
        self.res_scale.addItem("")
        self.res_scale.addItem("")
        self.res_scale.addItem("")
        self.res_scale.addItem("")
        self.res_scale.addItem("")
        self.res_scale.addItem("")
        self.horizontalLayout_6.addWidget(self.res_scale)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pixel_aspect_label = QtGui.QLabel(lazySiouxsie)
        self.pixel_aspect_label.setObjectName("pixel_aspect_label")
        self.horizontalLayout_8.addWidget(self.pixel_aspect_label)
        self.pixel_aspect = QtGui.QLineEdit(lazySiouxsie)
        self.pixel_aspect.setMaximumSize(QtCore.QSize(60, 16777215))
        self.pixel_aspect.setObjectName("pixel_aspect")
        self.horizontalLayout_8.addWidget(self.pixel_aspect)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.render_engine_label = QtGui.QLabel(lazySiouxsie)
        self.render_engine_label.setObjectName("render_engine_label")
        self.horizontalLayout_7.addWidget(self.render_engine_label)
        self.rendering_engine = QtGui.QComboBox(lazySiouxsie)
        self.rendering_engine.setObjectName("rendering_engine")
        self.rendering_engine.addItem("")
        self.rendering_engine.addItem("")
        self.rendering_engine.addItem("")
        self.rendering_engine.addItem("")
        self.rendering_engine.addItem("")
        self.horizontalLayout_7.addWidget(self.rendering_engine)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.quality_label = QtGui.QLabel(lazySiouxsie)
        self.quality_label.setObjectName("quality_label")
        self.horizontalLayout_10.addWidget(self.quality_label)
        self.quality_slider = QtGui.QSlider(lazySiouxsie)
        self.quality_slider.setMinimum(50)
        self.quality_slider.setMaximum(100)
        self.quality_slider.setProperty("value", 85)
        self.quality_slider.setOrientation(QtCore.Qt.Horizontal)
        self.quality_slider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.quality_slider.setObjectName("quality_slider")
        self.horizontalLayout_10.addWidget(self.quality_slider)
        self.quality_value = QtGui.QSpinBox(lazySiouxsie)
        self.quality_value.setProperty("value", 85)
        self.quality_value.setObjectName("quality_value")
        self.horizontalLayout_10.addWidget(self.quality_value)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem4)
        self.scene_lights = QtGui.QCheckBox(lazySiouxsie)
        self.scene_lights.setEnabled(False)
        self.scene_lights.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.scene_lights.setChecked(False)
        self.scene_lights.setObjectName("scene_lights")
        self.horizontalLayout_9.addWidget(self.scene_lights)
        self.ground_plane = QtGui.QCheckBox(lazySiouxsie)
        self.ground_plane.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ground_plane.setChecked(True)
        self.ground_plane.setObjectName("ground_plane")
        self.horizontalLayout_9.addWidget(self.ground_plane)
        self.chrome_balls = QtGui.QCheckBox(lazySiouxsie)
        self.chrome_balls.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.chrome_balls.setObjectName("chrome_balls")
        self.horizontalLayout_9.addWidget(self.chrome_balls)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.build_progress = QtGui.QProgressBar(lazySiouxsie)
        self.build_progress.setStyleSheet("QProgressBar {\n"
"    text-align: center;\n"
"    color: rgb(90, 90, 90);\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(224, 149, 0);\n"
"    width: 20px;\n"
"    margin: 1px;\n"
"}")
        self.build_progress.setProperty("value", 24)
        self.build_progress.setObjectName("build_progress")
        self.verticalLayout.addWidget(self.build_progress)
        self.status_label = QtGui.QLabel(lazySiouxsie)
        self.status_label.setObjectName("status_label")
        self.verticalLayout.addWidget(self.status_label)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.cancel_btn = QtGui.QPushButton(lazySiouxsie)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout_4.addWidget(self.cancel_btn)
        self.spin_btn = QtGui.QPushButton(lazySiouxsie)
        self.spin_btn.setObjectName("spin_btn")
        self.horizontalLayout_4.addWidget(self.spin_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.file_label.setBuddy(self.file_path)
        self.hdri_label.setBuddy(self.hdriList)
        self.custom.setBuddy(self.custom_hdri)
        self.startLabel.setBuddy(self.startFrame)
        self.endLabel.setBuddy(self.endFrame)
        self.totalFrameLabel.setBuddy(self.total_frames)
        self.resolution_label.setBuddy(self.res_width)
        self.pixel_aspect_label.setBuddy(self.pixel_aspect)
        self.render_engine_label.setBuddy(self.rendering_engine)
        self.quality_label.setBuddy(self.quality_slider)

        self.retranslateUi(lazySiouxsie)
        self.hdriList.setCurrentRow(-1)
        self.res_scale.setCurrentIndex(3)
        QtCore.QObject.connect(self.quality_slider, QtCore.SIGNAL("valueChanged(int)"), self.quality_value.setValue)
        QtCore.QObject.connect(self.quality_value, QtCore.SIGNAL("valueChanged(int)"), self.quality_slider.setValue)
        QtCore.QMetaObject.connectSlotsByName(lazySiouxsie)

    def retranslateUi(self, lazySiouxsie):
        lazySiouxsie.setWindowTitle(QtGui.QApplication.translate("lazySiouxsie", "Lazy Siouzsie", None))
        self.title.setText(QtGui.QApplication.translate("lazySiouxsie", "Lazy Siouxsie", None))
        self.subTitle.setText(QtGui.QApplication.translate("lazySiouxsie", "Auto Turntable Machine", None))
        self.file_label.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "The current file being Turn Tabled", None))
        self.file_label.setText(QtGui.QApplication.translate("lazySiouxsie", "File", None))
        self.file_path.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "The current file being Turn Tabled", None))
        self.file_path.setPlaceholderText(QtGui.QApplication.translate("lazySiouxsie", "The Current File to be sent to the farm", None))
        self.hdri_label.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "HDRII list provided by a Shotgun directory of Studio HDRIs", None))
        self.hdri_label.setText(QtGui.QApplication.translate("lazySiouxsie", "HDRIs", None))
        self.hdriList.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "HDRII list provided by a Shotgun directory of Studio HDRIs", None))
        self.custom.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "Custom HDRI file, if a specific file is desired", None))
        self.custom.setText(QtGui.QApplication.translate("lazySiouxsie", "Custom HDRI", None))
        self.custom_hdri.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "Custom HDRI file, if a specific file is desired", None))
        self.custom_hdri.setPlaceholderText(QtGui.QApplication.translate("lazySiouxsie", "If a show/shot specific HDRI is needed", None))
        self.browse_btn.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "Custom HDRI file, if a specific file is desired", None))
        self.browse_btn.setText(QtGui.QApplication.translate("lazySiouxsie", "Browse", None))
        self.frame_statement.setText(QtGui.QApplication.translate("lazySiouxsie", "The Start and End times are for the initial rotation.  A second rotation of equal time will be added to spin the HDRI around the object.  The Total Frames represents first and second rotations for each HDRI", None))
        self.startLabel.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "Starting frame of Camera animation.", None))
        self.startLabel.setText(QtGui.QApplication.translate("lazySiouxsie", "Start Frame", None))
        self.startFrame.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "Starting frame of Camera animation.", None))
        self.endLabel.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "End frame of the Camera Animation.  HDRI Spin will be added to this time", None))
        self.endLabel.setText(QtGui.QApplication.translate("lazySiouxsie", "End Frame", None))
        self.endFrame.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "End frame of the Camera Animation.  HDRI Spin will be added to this time", None))
        self.totalFrameLabel.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "Total frames of animation is the Camera Rotation plus an HDRI rotation of the same value.  Thus, double the frames", None))
        self.totalFrameLabel.setText(QtGui.QApplication.translate("lazySiouxsie", "Total Frames:", None))
        self.total_frames.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "Total frames of animation is the Camera Rotation plus an HDRI rotation of the same value.  Thus, double the frames", None))
        self.total_frames.setText(QtGui.QApplication.translate("lazySiouxsie", "240", None))
        self.resolution_label.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "Resolution set by Shotgun if available", None))
        self.resolution_label.setText(QtGui.QApplication.translate("lazySiouxsie", "Resolution", None))
        self.res_width.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "Resolution set by Shotgun if available", None))
        self.x_label.setText(QtGui.QApplication.translate("lazySiouxsie", "X", None))
        self.res_height.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "Resolution set by Shotgun if available", None))
        self.res_scale.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "Resolution scale will change the final render size.", None))
        self.res_scale.setItemText(0, QtGui.QApplication.translate("lazySiouxsie", "25%", None))
        self.res_scale.setItemText(1, QtGui.QApplication.translate("lazySiouxsie", "50%", None))
        self.res_scale.setItemText(2, QtGui.QApplication.translate("lazySiouxsie", "75%", None))
        self.res_scale.setItemText(3, QtGui.QApplication.translate("lazySiouxsie", "100%", None))
        self.res_scale.setItemText(4, QtGui.QApplication.translate("lazySiouxsie", "150%", None))
        self.res_scale.setItemText(5, QtGui.QApplication.translate("lazySiouxsie", "200%", None))
        self.pixel_aspect_label.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "Pixel aspect set by Shotgun if it\'s available", None))
        self.pixel_aspect_label.setText(QtGui.QApplication.translate("lazySiouxsie", "Pixel Aspect", None))
        self.pixel_aspect.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "Pixel aspect set by Shotgun if it\'s available", None))
        self.pixel_aspect.setText(QtGui.QApplication.translate("lazySiouxsie", "1.0", None))
        self.render_engine_label.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "The Rendering Engine.  Selected by Shotgun if it is available.", None))
        self.render_engine_label.setText(QtGui.QApplication.translate("lazySiouxsie", "Rendering Engine", None))
        self.rendering_engine.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "The Rendering Engine.  Selected by Shotgun if it is available.", None))
        self.rendering_engine.setItemText(0, QtGui.QApplication.translate("lazySiouxsie", "arnold", None))
        self.rendering_engine.setItemText(1, QtGui.QApplication.translate("lazySiouxsie", "vray", None))
        self.rendering_engine.setItemText(2, QtGui.QApplication.translate("lazySiouxsie", "redshift", None))
        self.rendering_engine.setItemText(3, QtGui.QApplication.translate("lazySiouxsie", "renderman", None))
        self.rendering_engine.setItemText(4, QtGui.QApplication.translate("lazySiouxsie", "mayasoftware", None))
        self.quality_label.setText(QtGui.QApplication.translate("lazySiouxsie", "Quality", None))
        self.scene_lights.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "When checked, any lights created in the scene will be rendered as one of the render passes.  Otherwise the existing lights will be ignored.", None))
        self.scene_lights.setText(QtGui.QApplication.translate("lazySiouxsie", "Use Scene Lights", None))
        self.ground_plane.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "Create a shadow catching ground plane", None))
        self.ground_plane.setText(QtGui.QApplication.translate("lazySiouxsie", "Ground Plane", None))
        self.chrome_balls.setText(QtGui.QApplication.translate("lazySiouxsie", "Auto Chrome Balls", None))
        self.status_label.setText(QtGui.QApplication.translate("lazySiouxsie", "Ready...", None))
        self.cancel_btn.setText(QtGui.QApplication.translate("lazySiouxsie", "Cancel", None))
        self.spin_btn.setToolTip(QtGui.QApplication.translate("lazySiouxsie", "Create the Turnable file and submit it.", None))
        self.spin_btn.setText(QtGui.QApplication.translate("lazySiouxsie", "Spin It", None))

