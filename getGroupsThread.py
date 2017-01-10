# -*- coding: utf-8 -*-

import paramiko
import socket
import re
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GetGroupsThread(QThread):
    '''Le thread qui fait le travail'''
    success = pyqtSignal()
    socketErr = pyqtSignal()
    authErr = pyqtSignal()

    def __init__(self,parent=None):
        QThread.__init__(self)
        self.parent=parent

    def setPassword(self,admin,password,ip):
        '''Méthode pour initialiser le mot de passe ssh'''
        self.adminLogin=admin
        self.password=password
        self.ip=ip

    def run(self):
        '''Méthode lancée au démarrage du thread, qui fait le boulot'''
        sshTest=paramiko.SSHClient()
        sshTest.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:    # On essaye la connexion avec un timeout de 6s
            sshTest.connect(self.ip,username='%s'%self.adminLogin,password='%s'%self.password,timeout=6)

            # On récupère l'année
            stdin, stdout, stderr = sshTest.exec_command("sudo tail /usr/local/ANNEE")

            anneeData = stdout.read().splitlines()
            for line in anneeData:
                if re.match(b'^(annee=(?:[0-9]{4}))',line):
                    annee=line[6:].decode("utf-8")
            self.parent.annee=annee # On l'assigne à la variable du parent

            # On récupère la liste des groupes
            stdin, stdout, stderr = sshTest.exec_command("sudo ldapsearch -xLLL '(&(objectClass=posixGroup)(cn=*))' cn")
            data = stdout.read().splitlines()
            classeList=[]
            groupList=[]
            groupesAEnlever=["Account Operators","Administrators","Backup Operators","Domain Admins",
                                                "Domain Computers","Domain Guests","Domain Users",
                                                    "Print Operators","Replicators"]
            for line in data:
                if re.match(b'^(cn: (?![0-9]{4}_))',line):
                    if line[3:].decode("utf-8").strip() not in groupesAEnlever:
                        groupList.append(line[3:].decode("utf-8").strip())
                if re.match('^(cn: (?=%s_))'%annee,line.decode("utf-8")):
                    classeList.append(line[9:].decode("utf-8").strip())

            self.parent.classesList=classeList
            self.parent.groupesList=groupList

            self.success.emit()
        except socket.error:
            self.socketErr.emit()
            return
        except paramiko.AuthenticationException:
            self.authErr.emit()
            return
        sshTest.close()
        return
