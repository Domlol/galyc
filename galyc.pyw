#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Modules généraux
import paramiko
from PyQt5.QtWidgets import *
import socket
import unicodedata
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Sources propres à Galyc
from profThread import *    # Classe du thread prof
from eleveThread import *    # Classe du thread élève
from compteThread import *    # Classe du thread compte
from groupeThread import *    # Classe du thread groupe
from getGroupsThread import * # Thread qui récupère la liste des groupes et classes
from mdpDialog import *     # Classe du dialogue mot de passe
import ui_galycDialog  # L'UI

# Fichier de ressources (images...)
import ressources_rc

class Galyc(QDialog, ui_galycDialog.Ui_galycDialog):
    '''Classe du widget principal'''
    def __init__(self, parent=None):

        # Constructeur de la classe parente
        super(Galyc, self).__init__(parent)

        # Initialisation de variables
        self.password=""                    # Mot de passe initialisé
        self.adminLogin=""
        self.test=False                     # Test du mot de passe 
        self.setupUi(self)                  # Initialisation de l'ui
        self.groupesList=[]
        self.classesList=[]
        self.annee=""

        self.ipDict={'Utilisation distante': '194.254.62.70','Utilisation locale': '10.186.21.2'}
        self.ipCombo.addItems(self.ipDict.keys())
        self.toolButton.setFocus()
        self.progressBar.setMaximum(100)
        self.progressBar.setVisible(False)

        # Connexions signaux/slots
        self.profButton.clicked.connect(self.ajoutProf)
        self.eleveButton.clicked.connect(self.ajoutEleve)
        self.groupeButton.clicked.connect(self.ajoutGroupe)
        self.supprGroupeButton.clicked.connect(self.supprGroupe)
        self.supprServButton.clicked.connect(self.supprService)
        self.addServButton.clicked.connect(self.ajoutService)
        self.compteButton.clicked.connect(self.infoCompte)
        self.toolButton.clicked.connect(self.onMdpClicked)
        self.totalList.itemActivated.connect(self.onGroupeDoucleClicked)
        self.aboutButton.clicked.connect(self.onAboutClicked)
        self.totalServiceList.itemActivated.connect(self.onServDoucleClicked)
        self.delButton.clicked.connect(self.onDelButtonClicked)
        self.delServButton.clicked.connect(self.onDelServButtonClicked)

    def ajoutProf(self):
        '''Slot du bouton ajout Prof'''

        # Vérification qu'aucun champ n'est vide
        if len(self.loginProf.text())==0 or len(self.prenomProf.text())==0 \
               or len(self.nomProf.text())==0 or len(self.courrielProf.text())==0:
            QMessageBox.warning(self, 
                u"Paramètre manquant", 
                u"Veuillez remplir tous les champs requis !")
            return

        # Vérification que le mot de passe a été testé
        if not self.test:
            QMessageBox.warning(self, 
                u"Entrez le mot de passe", 
                u"Le mot de passe n'a pas été validé !")
            return 
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(0)  # Progress Bar mise en marche
        self.textSortie.clear()         # On efface le texte de sortie

        ####
        # On lance le thread
        ####
        # Création de l'objet
        self.profThread = ProfThread()
        # Connexion au signal update du thread
        self.profThread.update['QString'].connect(self.add)
        self.profThread.finished.connect(self.stop)
        prenom=self.formatNoms(self.prenomProf.text())
        nom=self.formatNoms(self.nomProf.text()).upper()
        # Envoi des arguments au thread
        self.profThread.setArgs(self.loginProf.text(),
                                                        prenom,
                                                        nom,
                                        self.courrielProf.text())
        self.profThread.setPassword(self.adminLogin,self.password,self.ipDict[self.ipCombo.currentText()])
        self.profThread.start() # On le lance (lancement de run())

    def ajoutEleve(self):
        '''Slot du bouton ajout Eleve'''

        # Vérification qu'aucun champ n'est vide
        if len(self.loginEleve.text())==0 or len(self.prenomEleve.text())==0 \
               or len(self.nomEleve.text())==0 or len(self.classeEleve.text())==0 \
                                                        or len(self.mdpEleve.text())==0:
            QMessageBox.warning(self, 
                u"Paramètre manquant", 
                u"Veuillez remplir tous les champs requis !")
            return

        # Vérification que le mot de passe a été testé
        if not self.test:
            QMessageBox.warning(self, 
                u"Entrez le mot de passe", 
                u"Le mot de passe n'a pas été validé !")
            return 
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(0)  # Progress Bar mise en marche
        self.textSortie.clear()         # On efface le texte de sortie

        ####
        # On lance le thread
        ####
        # Création de l'objet
        self.eleveThread = EleveThread()
        # Connexion au signal update du thread
        self.eleveThread.update['QString'].connect(self.add)
        self.eleveThread.finished.connect(self.stop)
        # Envoi des arguments au thread
        prenom=self.formatNoms(self.prenomEleve.text())
        nom=self.formatNoms(self.nomEleve.text()).upper()
        self.eleveThread.setArgs(self.loginEleve.text(),
                                    prenom,
                                      nom,
                                        self.classeEleve.text(),
                                           self.mdpEleve.text())
        self.eleveThread.setPassword(self.adminLogin,self.password,self.ipDict[self.ipCombo.currentText()])
        self.eleveThread.start() # On le lance (lancement de run())
        
    def ajoutGroupe(self):
        '''Slot du bouton ajout Groupe'''

        # Vérification qu'aucun champ n'est vide
        if len(self.loginLine.text())==0 or self.groupList.count()==0:
            QMessageBox.warning(self, 
                u"Paramètre manquant", 
                u"Veuillez remplir tous les champs requis !")
            return

        groupsStr=self.getGroupsToAction()

        # Vérification que le mot de passe a été testé
        if not self.test:
            QMessageBox.warning(self, 
                u"Entrez le mot de passe", 
                u"Le mot de passe n'a pas été validé !")
            return 
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(0)  # Progress Bar mise en marche
        self.textSortie.clear()         # On efface le texte de sortie

        ####
        # On lance le thread
        ####
        # Création de l'objet
        self.groupeThread = GroupeThread("plus")
        # Connexion au signal update du thread
        self.groupeThread.update['QString'].connect(self.add)
        self.groupeThread.finished.connect(self.stop)
        # Envoi des arguments au thread
        self.groupeThread.setArgs(self.loginLine.text(),groupsStr)
        self.groupeThread.setPassword(self.adminLogin,self.password,self.ipDict[self.ipCombo.currentText()])
        self.groupeThread.start() # On le lance (lancement de run())

    def supprGroupe(self):
        '''Slot du bouton supprimer Groupe'''
        # Vérification qu'aucun champ n'est vide
        if len(self.loginLine.text())==0 or self.groupList.count()==0:
            QMessageBox.warning(self,
                u"Paramètre manquant",
                u"Veuillez remplir tous les champs requis !")
            return

        groupsStr=self.getGroupsToAction()

        # Vérification que le mot de passe a été testé
        if not self.test:
            QMessageBox.warning(self,
                u"Entrez le mot de passe",
                u"Le mot de passe n'a pas été validé !")
            return
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(0)  # Progress Bar mise en marche
        self.textSortie.clear()         # On efface le texte de sortie

        ####
        # On lance le thread
        ####
        # Création de l'objet
        self.groupeThread = GroupeThread("moins")
        # Connexion au signal update du thread
        self.groupeThread.update['QString'].connect(self.add)
        self.groupeThread.finished.connect(self.stop)
        # Envoi des arguments au thread
        self.groupeThread.setArgs(self.loginLine.text(),groupsStr)
        self.groupeThread.setPassword(self.adminLogin,self.password,self.ipDict[self.ipCombo.currentText()])
        self.groupeThread.start() # On le lance (lancement de run())

    def getGroupsToAction(self):
        str=self.groupList.item(0).text()
        for i in range(1,self.groupList.count()):
            str += ",%s"%self.groupList.item(i).text()
        return str

    def getServicesToAction(self):
        str=self.serviceList.item(0).text()
        for i in range(1,self.serviceList.count()):
            str += ",%s"%self.serviceList.item(i).text()
        return str

    def onGroupeDoucleClicked(self,item):
        self.groupList.addItem(item.text())

    def ajoutService(self):
        '''Slot du bouton ajout Service'''

        # Vérification qu'aucun champ n'est vide
        if len(self.loginLine.text())==0 or self.serviceList.count()==0:
            QMessageBox.warning(self,
                u"Paramètre manquant",
                u"Veuillez remplir tous les champs requis !")
            return

        servStr=self.getServicesToAction()

        # Vérification que le mot de passe a été testé
        if not self.test:
            QMessageBox.warning(self,
                u"Entrez le mot de passe",
                u"Le mot de passe n'a pas été validé !")
            return
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(0)  # Progress Bar mise en marche
        self.textSortie.clear()         # On efface le texte de sortie

        ####
        # On lance le thread
        ####
        # Création de l'objet
        self.groupeThread = GroupeThread("servplus")
        # Connexion au signal update du thread
        self.groupeThread.update['QString'].connect(self.add)
        self.groupeThread.finished.connect(self.stop)
        # Envoi des arguments au thread
        self.groupeThread.setArgs(self.loginLine.text(),servStr)
        self.groupeThread.setPassword(self.adminLogin,self.password,self.ipDict[self.ipCombo.currentText()])
        self.groupeThread.start() # On le lance (lancement de run())

    def supprService(self):
        '''Slot du bouton supprimer Groupe'''

        # Vérification qu'aucun champ n'est vide
        if len(self.loginLine.text())==0 or self.serviceList.count()==0:
            QMessageBox.warning(self,
                u"Paramètre manquant",
                u"Veuillez remplir tous les champs requis !")
            return

        servStr=self.getServicesToAction()

        # Vérification que le mot de passe a été testé
        if not self.test:
            QMessageBox.warning(self,
                u"Entrez le mot de passe",
                u"Le mot de passe n'a pas été validé !")
            return
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(0)  # Progress Bar mise en marche
        self.textSortie.clear()         # On efface le texte de sortie

        ####
        # On lance le thread
        ####
        # Création de l'objet
        self.groupeThread = GroupeThread("servmoins")
        # Connexion au signal update du thread
        self.groupeThread.update['QString'].connect(self.add)
        self.groupeThread.finished.connect(self.stop)
        # Envoi des arguments au thread
        self.groupeThread.setArgs(self.loginLine.text(),servStr)
        self.groupeThread.setPassword(self.adminLogin,self.password,self.ipDict[self.ipCombo.currentText()])
        self.groupeThread.start() # On le lance (lancement de run())

    def onServDoucleClicked(self,item):
        self.serviceList.addItem(item.text())

    def onDelButtonClicked(self):
        itemList=self.groupList.selectedItems()
        for item in itemList:
            self.groupList.takeItem(self.groupList.row(item))

    def onDelServButtonClicked(self):
        itemList=self.serviceList.selectedItems()
        for item in itemList:
            self.serviceList.takeItem(self.serviceList.row(item))

    def infoCompte(self):
        '''Slot du bouton Informations compte'''

        # Vérification qu'aucun champ n'est vide
        if len(self.loginLine.text())==0:
            QMessageBox.warning(self, 
                u"Paramètre manquant", 
                u"Veuillez remplir tous les champs requis !")
            return


        # Vérification que le mot de passe a été testé
        if not self.test:
            QMessageBox.warning(self, 
                u"Entrez le mot de passe", 
                u"Le mot de passe n'a pas été validé !")
            return 
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(0)  # Progress Bar mise en marche
        self.textSortie.clear()         # On efface le texte de sortie

        ####
        # On lance le thread
        ####
        # Création de l'objet
        self.compteThread = CompteThread()
        # Connexion au signal update du thread
        self.compteThread.update['QString'].connect(self.add)
        self.compteThread.finished.connect(self.stop)
        # Envoi des arguments au thread
        self.compteThread.setArgs(self.loginLine.text())
        self.compteThread.setPassword(self.adminLogin,self.password,self.ipDict[self.ipCombo.currentText()])
        self.compteThread.start() # On le lance (lancement de run())

    def stop(self):
        '''On remet en veille la progressBar'''
        self.progressBar.setVisible(False)
        self.progressBar.setMaximum(100)

    def add(self,text):
        '''Slot qui ajoute du texte à textSortie'''
        self.textSortie.append(text)

    def onMdpClicked(self):
        '''Création du dialogue Mot de passe'''
        mdpDialog = MdpDialog(parent=self)
        ##### Temporaire :
        mdpDialog.lineAdmin.setText(u"script")
        mdpDialog.lineAdmin.hide()
        mdpDialog.labelAdmin.hide()
        #####
        mdpDialog.mdpSend.connect(self.mdpSent)
        mdpDialog.show()

    def mdpSent(self):
        """Slot correspondant au clic Ok du dialogue mot de passe
        et qui teste la connexion"""
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(0)
        self.getGroups = GetGroupsThread(self)
        self.getGroups.finished.connect(self.stop)
        self.getGroups.success.connect(self.updatePwd)
        self.getGroups.socketErr.connect(self.socketError)
        self.getGroups.authErr.connect(self.authError)
        self.getGroups.setPassword(self.adminLogin,self.password,self.ipDict[self.ipCombo.currentText()])
        self.getGroups.start()

    def updatePwd(self):
        """Après que le mdp eu été testé avec succès, le thread met à jour
        les variables groupesList, classesList et année et ce slot est appelé"""
    #    self.toolButton.setText(u"Connexion au serveur testée avec succès")
        self.toolButton.setIcon(QIcon(":/images/images/unlock.png"))
        self.test=True
        self.groupesList.sort()
        self.classesList.sort()
        self.totalList.addItems(self.groupesList)
        self.totalServiceList.addItems(self.classesList)

    def socketError(self):
        QMessageBox.warning(self,
            u"Connexion refusée",
            u"Veuillez vérifier votre connexion et l'état du serveur!")

    def authError(self):
        QMessageBox.warning(self,
            u"Connexion refusée",
            u"Problème d'authentification. Vérifiez votre mot de passe !")

    def onAboutClicked(self):
        QMessageBox.about(self,
            u"A propos de Galyc",
            u"<center><b>Galyc</b> est développé par <a href=\"mailto:gwencleon@gmail.com\">Gwenaël Cléon</a> \
            à l'aide de PyQt5. \
            <p>Version 1.0.22</center>")

    def formatNoms(self,input_str):
        eudanlo=u"\u0153"
        eudanla=u"\u00E6"
        input_str=input_str.replace(eudanlo,'oe')
        input_str=input_str.replace(eudanla,'ae')
        nkfd_form = unicodedata.normalize('NFKD', input_str)
        str1 = nkfd_form.encode('ASCII', 'ignore')
        str2=re.sub(r'\s+','_',str1)
        str3=str2.replace(r"'",'_')
        return str3

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    galyc=Galyc()
    galyc.show()
    app.exec_()
