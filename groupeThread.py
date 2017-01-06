# -*- coding: utf-8 -*-

import paramiko
import socket
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class GroupeThread(QThread):
    '''Le thread qui fait le travail'''
    update = pyqtSignal('QString')

    def __init__(self,actionStr):
        QThread.__init__(self)
        self.actionStr=actionStr

    def setArgs(self,login,groupes):
        '''Méthode pour initialiser les arguments'''
        self.login=login
        self.groupes=groupes

    def setPassword(self,admin,password,ip):
        '''Méthode pour initialiser le mot de passe ssh'''
        self.adminLogin=admin
        self.password=password
        self.ip=ip

    def run(self):
        '''Méthode lancée au démarrage du thread, qui fait le boulot'''
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.actionStr=="plus":
            command="sudo /usr/local/sbin/groupes+ -e %s %s"%(self.login,self.groupes)
            outMsg=u"Groupe(s) ajouté(s) avec succès"
        elif self.actionStr=="moins":
            command="sudo /usr/local/sbin/groupes- -e %s %s"%(self.login,self.groupes)
            outMsg=u"Groupe(s) supprimé(s) avec succès"
        elif self.actionStr=="servplus":
            command="sudo /usr/local/sbin/service+ -e %s %s"%(self.login,self.groupes)
            outMsg=u"Services(s) ajouté(s) avec succès"
        elif self.actionStr=="servmoins":
            command="sudo /usr/local/sbin/service- -e %s %s"%(self.login,self.groupes)
            outMsg=u"Services(s) supprimé(s) avec succès"
        try:
            ssh.connect(self.ip,username='%s'%self.adminLogin,password='%s'%self.password,timeout=10)
            stdin, stdout, stderr = ssh.exec_command(command)
            data = stdout.read().splitlines()
        except socket.error:
            self.update.emit(u"Problème de connexion.")
            self.update.emit(u"Vérifiez votre accès au réseau et l'état du serveur.")
            return
        except paramiko.AuthenticationException:
            self.update.emit(u"Problème d'authentification.")
            self.update.emit(u"Vérifiez votre mot de passe.")
            return

        if len(data)==0:
            self.update.emit(outMsg)
            return
			
        # On envoie les résultats à l'ui principale
        for line in data:
            self.update.emit(line.decode("utf-8"))
        ssh.close()
        return
