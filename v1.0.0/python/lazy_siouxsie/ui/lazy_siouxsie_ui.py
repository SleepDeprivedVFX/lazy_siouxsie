# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\sleep\OneDrive\Documents\shotgun\mastertemplate\install\manual\tk-lazy_siouxsie\v1.0.0\python\lazy_siouxsie\ui\lazy_siouxsie_ui.ui'
#
# Created: Sat Jun 30 19:11:46 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from sgtk.platform.qt import QtCore, QtGui

class Ui_lazySiouxsie(object):
    def setupUi(self, lazySiouxsie):
        lazySiouxsie.setObjectName("lazySiouxsie")
        lazySiouxsie.resize(557, 427)
        self.verticalLayout = QtGui.QVBoxLayout(lazySiouxsie)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtGui.QLabel(lazySiouxsie)
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.file_label = QtGui.QLabel(lazySiouxsie)
        self.file_label.setObjectName("file_label")
        self.horizontalLayout_5.addWidget(self.file_label)
        self.file_path = QtGui.QLineEdit(lazySiouxsie)
        self.file_path.setObjectName("file_path")
        self.horizontalLayout_5.addWidget(self.file_path)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
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
        self.verticalLayout.addLayout(self.horizontalLayout)
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
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.frame_statement = QtGui.QLabel(lazySiouxsie)
        self.frame_statement.setWordWrap(True)
        self.frame_statement.setObjectName("frame_statement")
        self.verticalLayout.addWidget(self.frame_statement)
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
        self.verticalLayout.addLayout(self.horizontalLayout_2)
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
        self.verticalLayout.addLayout(self.horizontalLayout_6)
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
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.cancel_btn = QtGui.QPushButton(lazySiouxsie)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout_4.addWidget(self.cancel_btn)
        self.spin_btn = QtGui.QPushButton(lazySiouxsie)
        self.spin_btn.setObjectName("spin_btn")
        self.horizontalLayout_4.addWidget(self.spin_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(lazySiouxsie)
        self.hdriList.setCurrentRow(-1)
        self.res_scale.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(lazySiouxsie)

    def retranslateUi(self, lazySiouxsie):
        lazySiouxsie.setWindowTitle(QtGui.QApplication.translate("lazySiouxsie", "Lazy Siouzsie", None))
        self.title.setText(QtGui.QApplication.translate("lazySiouxsie", "Lazy Siouxsie", None))
        self.file_label.setText(QtGui.QApplication.translate("lazySiouxsie", "File", None))
        self.file_path.setPlaceholderText(QtGui.QApplication.translate("lazySiouxsie", "The Current File to be sent to the farm", None))
        self.hdri_label.setText(QtGui.QApplication.translate("lazySiouxsie", "HDRIs", None))
        self.custom.setText(QtGui.QApplication.translate("lazySiouxsie", "Custom HDRI", None))
        self.custom_hdri.setPlaceholderText(QtGui.QApplication.translate("lazySiouxsie", "If a show/shot specific HDRI is needed", None))
        self.browse_btn.setText(QtGui.QApplication.translate("lazySiouxsie", "Browse", None))
        self.frame_statement.setText(QtGui.QApplication.translate("lazySiouxsie", "The Start and End times are for the initial rotation.  A second rotation of equal time will be added to spin the HDRI around the object.  The Total Frames represents first and second rotations for each HDRI", None))
        self.startLabel.setText(QtGui.QApplication.translate("lazySiouxsie", "Start Frame", None))
        self.endLabel.setText(QtGui.QApplication.translate("lazySiouxsie", "End Frame", None))
        self.totalFrameLabel.setText(QtGui.QApplication.translate("lazySiouxsie", "Total Frames:", None))
        self.total_frames.setText(QtGui.QApplication.translate("lazySiouxsie", "240", None))
        self.resolution_label.setText(QtGui.QApplication.translate("lazySiouxsie", "Resolution", None))
        self.x_label.setText(QtGui.QApplication.translate("lazySiouxsie", "X", None))
        self.res_scale.setItemText(0, QtGui.QApplication.translate("lazySiouxsie", "25%", None))
        self.res_scale.setItemText(1, QtGui.QApplication.translate("lazySiouxsie", "50%", None))
        self.res_scale.setItemText(2, QtGui.QApplication.translate("lazySiouxsie", "75%", None))
        self.res_scale.setItemText(3, QtGui.QApplication.translate("lazySiouxsie", "100%", None))
        self.res_scale.setItemText(4, QtGui.QApplication.translate("lazySiouxsie", "150%", None))
        self.res_scale.setItemText(5, QtGui.QApplication.translate("lazySiouxsie", "200%", None))
        self.render_engine_label.setText(QtGui.QApplication.translate("lazySiouxsie", "Rendering Engine", None))
        self.rendering_engine.setItemText(0, QtGui.QApplication.translate("lazySiouxsie", "arnold", None))
        self.rendering_engine.setItemText(1, QtGui.QApplication.translate("lazySiouxsie", "vray", None))
        self.rendering_engine.setItemText(2, QtGui.QApplication.translate("lazySiouxsie", "redshift", None))
        self.rendering_engine.setItemText(3, QtGui.QApplication.translate("lazySiouxsie", "renderman", None))
        self.rendering_engine.setItemText(4, QtGui.QApplication.translate("lazySiouxsie", "mayasoftware", None))
        self.cancel_btn.setText(QtGui.QApplication.translate("lazySiouxsie", "Cancel", None))
        self.spin_btn.setText(QtGui.QApplication.translate("lazySiouxsie", "Spin It", None))
