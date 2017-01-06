# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import ui_mdpDialog

class MdpDialog(QDialog, ui_mdpDialog.Ui_mdpDialog):
    '''Classe du dialogue mot de passe'''
    mdpSend = pyqtSignal()

    def __init__(self, parent=None):
        '''Constructeur'''
        self.parent=parent  # On récupère la référence au dialogue principal
        super(MdpDialog, self).__init__(parent)
        self.setupUi(self)
        self.okButton.clicked.connect(self.getPass)

    def getPass(self):
        '''Exécuté quand on clic sur Ok'''
#        self.password = unicode(self.mdpEdit.text())
        self.password = self.mdpEdit.text()
        print(self.password)
#        self.adminLogin=unicode(self.lineAdmin.text())
        self.adminLogin = self.lineAdmin.text()
        if len(self.password)==0:
            QMessageBox.warning(self, "", "Remplissez le champ \"Mot de passe\" !")
        elif len(self.adminLogin)==0:
            QMessageBox.warning(self, "", "Remplissez le champ \"Votre login\" !")
        else:
            # On initialise la variable password de la classe parente (Galyc)
            self.parent.password=self.password
            self.parent.adminLogin=self.adminLogin
            self.mdpSend.emit()
            self.close()
