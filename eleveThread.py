# -*- coding: utf-8 -*-

import paramiko
import socket
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class EleveThread(QThread):
    '''Le thread qui fait le travail'''
    update = pyqtSignal('QString')

    def __init__(self):
        QThread.__init__(self)

    def setArgs(self,login,prenom,nom,classe,mdp):
        '''Méthode pour initialiser les arguments'''
        self.login=login
        self.prenom=prenom
        self.nom=nom
        self.classe=classe
        self.mdp=mdp

    def setPassword(self,admin,password,ip):
        '''Méthode pour initialiser le mot de passe ssh'''
        self.adminLogin=admin
        self.password=password
        self.ip=ip

    def run(self):
        '''Méthode lancée au démarrage du thread, qui fait le boulot'''
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.ip,username='%s'%self.adminLogin,password='%s'%self.password,timeout=10)
            stdin, stdout, stderr = ssh.exec_command("sudo /usr/local/sbin/nouveleve -e \
                                                        %s %s %s %s %s"%(self.login,
                                                                        self.prenom,
                                                                            self.nom,
                                                                                self.classe,
                                                                                    self.mdp))
            data = stdout.read().splitlines()
        except socket.error:
            self.update.emit(u"Problème de connexion.")
            self.update.emit(u"Vérifiez votre accès au réseau et l'état du serveur.")
            return
        except paramiko.AuthenticationException:
            self.update.emit(u"Problème d'authentification.")
            self.update.emit(u"Vérifiez votre mot de passe.")
            return

        # On envoie les résultats à l'ui principal
        for line in data:
            self.update.emit(line.decode("utf-8"))
        return
