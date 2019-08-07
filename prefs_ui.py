# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prefs_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PrefsDialog(object):
    def setupUi(self, PrefsDialog):
        PrefsDialog.setObjectName("PrefsDialog")
        PrefsDialog.resize(568, 296)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(PrefsDialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(PrefsDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lbl_scan_folder = QtWidgets.QLabel(self.groupBox)
        self.lbl_scan_folder.setObjectName("lbl_scan_folder")
        self.horizontalLayout_2.addWidget(self.lbl_scan_folder)
        self.ln_scan_folder_path = QtWidgets.QLineEdit(self.groupBox)
        self.ln_scan_folder_path.setMinimumSize(QtCore.QSize(350, 0))
        self.ln_scan_folder_path.setReadOnly(True)
        self.ln_scan_folder_path.setObjectName("ln_scan_folder_path")
        self.horizontalLayout_2.addWidget(self.ln_scan_folder_path)
        self.btn_browse_scan = QtWidgets.QPushButton(self.groupBox)
        self.btn_browse_scan.setObjectName("btn_browse_scan")
        self.horizontalLayout_2.addWidget(self.btn_browse_scan)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lbl_work_folder = QtWidgets.QLabel(self.groupBox)
        self.lbl_work_folder.setObjectName("lbl_work_folder")
        self.horizontalLayout_3.addWidget(self.lbl_work_folder)
        self.ln_work_folder_path = QtWidgets.QLineEdit(self.groupBox)
        self.ln_work_folder_path.setMinimumSize(QtCore.QSize(350, 0))
        self.ln_work_folder_path.setReadOnly(True)
        self.ln_work_folder_path.setObjectName("ln_work_folder_path")
        self.horizontalLayout_3.addWidget(self.ln_work_folder_path)
        self.btn_browse_work = QtWidgets.QPushButton(self.groupBox)
        self.btn_browse_work.setObjectName("btn_browse_work")
        self.horizontalLayout_3.addWidget(self.btn_browse_work)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(PrefsDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lbl_server_port = QtWidgets.QLabel(self.groupBox_2)
        self.lbl_server_port.setObjectName("lbl_server_port")
        self.horizontalLayout_4.addWidget(self.lbl_server_port)
        self.ln_web_server_port = QtWidgets.QLineEdit(self.groupBox_2)
        self.ln_web_server_port.setMaximumSize(QtCore.QSize(75, 16777215))
        self.ln_web_server_port.setInputMask("")
        self.ln_web_server_port.setObjectName("ln_web_server_port")
        self.horizontalLayout_4.addWidget(self.ln_web_server_port)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(PrefsDialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.chk_debug_logs = QtWidgets.QCheckBox(self.groupBox_3)
        self.chk_debug_logs.setObjectName("chk_debug_logs")
        self.verticalLayout_3.addWidget(self.chk_debug_logs)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btn_Cancel = QtWidgets.QPushButton(PrefsDialog)
        self.btn_Cancel.setObjectName("btn_Cancel")
        self.horizontalLayout.addWidget(self.btn_Cancel)
        self.btn_OK = QtWidgets.QPushButton(PrefsDialog)
        self.btn_OK.setDefault(True)
        self.btn_OK.setObjectName("btn_OK")
        self.horizontalLayout.addWidget(self.btn_OK)
        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.retranslateUi(PrefsDialog)
        self.btn_Cancel.clicked.connect(PrefsDialog.reject)
        self.btn_OK.clicked.connect(PrefsDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(PrefsDialog)

    def retranslateUi(self, PrefsDialog):
        _translate = QtCore.QCoreApplication.translate
        PrefsDialog.setWindowTitle(_translate("PrefsDialog", "ALS preferences"))
        self.groupBox.setTitle(_translate("PrefsDialog", "Pathes"))
        self.lbl_scan_folder.setText(_translate("PrefsDialog", "Scan folder :"))
        self.btn_browse_scan.setText(_translate("PrefsDialog", "Change..."))
        self.lbl_work_folder.setText(_translate("PrefsDialog", "Work folder :"))
        self.btn_browse_work.setText(_translate("PrefsDialog", "Change..."))
        self.groupBox_2.setTitle(_translate("PrefsDialog", "Web server"))
        self.lbl_server_port.setText(_translate("PrefsDialog", "Server port number (between 1024 & 65535) :"))
        self.groupBox_3.setTitle(_translate("PrefsDialog", "Misc"))
        self.chk_debug_logs.setText(_translate("PrefsDialog", "Debug logs (requires application restart)"))
        self.btn_Cancel.setText(_translate("PrefsDialog", "Cancel"))
        self.btn_OK.setText(_translate("PrefsDialog", "OK"))
