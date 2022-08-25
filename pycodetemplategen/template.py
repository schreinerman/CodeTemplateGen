
str = type('')
import os
import datetime
import threading
import warnings
import ctypes as ct
from pathlib import Path

scriptPath = os.path.dirname(os.path.abspath(__file__))
templatesPath = os.path.join(scriptPath,"templates")

class Template:
    @staticmethod
    def getFile(fileName,subTemplateDir=""):
        path = templatesPath
        if subTemplateDir:
            path = os.path.join(templatesPath,subTemplateDir)
        return os.path.join(path,fileName)
        

    @staticmethod
    def readFile(fileName,subTemplateDir=""):
        cFile = open(Template.getFile(fileName,subTemplateDir), 'r')
        tmp = cFile.read()
        cFile.close()
        return tmp

    @staticmethod
    def copyFile(fileName,toPath,subTemplateDir=""):
        toFile=os.path.join(toPath,os.path.basename(fileName))
        targetFile = open(toFile, 'w')
        targetFile.write(Template.readFile(fileName,subTemplateDir))
        targetFile.close()

    @staticmethod
    def copyFileReplaceVars(fileName,toPath,projectName,creator,company,subTemplateDir=""):
        toFile=os.path.join(toPath,os.path.basename(fileName))
        targetFile = open(toFile, 'w')
        content = Template.readFile(fileName,subTemplateDir)
        content = content.replace("%REPLACE_PROJECT_NAME%",projectName)
        content = content.replace("%REPLACE_CREATOR%",creator)
        content = content.replace("%REPLACE_COMPANY%",company)
        targetFile.write(content)
        targetFile.close()
        