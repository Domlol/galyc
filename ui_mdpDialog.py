# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mdpDialog.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mdpDialog(object):
    def setupUi(self, mdpDialog):
        mdpDialog.setObjectName("mdpDialog")
        mdpDialog.setWindowModality(QtCore.Qt.NonModal)
        mdpDialog.resize(432, 203)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/images/galyc.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mdpDialog.setWindowIcon(icon)
        mdpDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(mdpDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(mdpDialog)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.labelAdmin = QtWidgets.QLabel(mdpDialog)
        self.labelAdmin.setEnabled(True)
        self.labelAdmin.setObjectName("labelAdmin")
        self.gridLayout.addWidget(self.labelAdmin, 0, 0, 1, 1)
        self.lineAdmin = QtWidgets.QLineEdit(mdpDialog)
        self.lineAdmin.setEnabled(True)
        self.lineAdmin.setText("")
        self.lineAdmin.setObjectName("lineAdmin")
        self.gridLayout.addWidget(self.lineAdmin, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(98, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(mdpDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.mdpEdit = QtWidgets.QLineEdit(mdpDialog)
        self.mdpEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.mdpEdit.setObjectName("mdpEdit")
        self.gridLayout.addWidget(self.mdpEdit, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(98, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.okButton = QtWidgets.QPushButton(mdpDialog)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout_3.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(mdpDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_3.addWidget(self.cancelButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(mdpDialog)
        self.cancelButton.clicked.connect(mdpDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(mdpDialog)

    def retranslateUi(self, mdpDialog):
        _translate = QtCore.QCoreApplication.translate
        mdpDialog.setWindowTitle(_translate("mdpDialog", "Mot de passe Administrateur"))
        self.label.setText(_translate("mdpDialog", "Vous devez vous identifier et avoir des droits d\'administrateur pour utiliser Galyc"))
        self.labelAdmin.setText(_translate("mdpDialog", "Votre login :"))
        self.label_3.setText(_translate("mdpDialog", "Mot de passe :"))
        self.okButton.setText(_translate("mdpDialog", "Ok"))
        self.cancelButton.setText(_translate("mdpDialog", "Annuler"))

import ressources_rc
