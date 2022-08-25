from __future__ import (
    unicode_literals,
    print_function,
    division,
    absolute_import,
    )

from pycodetemplategen.cgenerator import CGenerator

# Make Py2's str and range equivalent to Py3's
str = type('')

import os
import datetime
import threading
import warnings
import ctypes as ct
from pathlib import Path
from pycodetemplategen.template import Template

class CMakeGenerator:
    @staticmethod 
    def checkCreatePath(path):
        if not os.path.exists(path):
            os.makedirs(path)
    @staticmethod
    def genCMakeLists(path,projectName,cpp=False):
        cmakeListsFileName = os.path.join(path,"CMakeLists.txt")
        cmakeListsContent = Template.readFile("CMakeLists.txt")
        cmakeListsContent = cmakeListsContent.replace("%REPLACE_PROJECT_NAME%",projectName)
        if cpp:
             cmakeListsContent = cmakeListsContent.replace("main.c","main.cpp")
        cmakeListsFile = open(cmakeListsFileName, 'w')
        cmakeListsFile.write(cmakeListsContent)
        cmakeListsFile.close()

    def genReadme(path,projectName):
        fileName = os.path.join(path,"README.md")
        content = Template.readFile("README.md")
        content = content.replace("%REPLACE_PROJECT_NAME%",projectName)
        fileHandle = open(fileName, 'w')
        fileHandle.write(content)
        fileHandle.close()

    def genDisclaimer(path,creator,company=""):
        fileName = os.path.join(path,"README.md")
        content = "Created by " + creator + "\r\n"
        content += "\r\n"
        content += "Copyright © " + str(datetime.datetime.now().year) + " " + company + ". All rights reserved.\r\n"
        content += Template.readFile("DISCLAIMER.md")
        fileHandle = open(fileName, 'w')
        fileHandle.write(content)
        fileHandle.close()

    @staticmethod
    def createProject(path,projectName,creator,description,disclaimer="",company="",cppMode=False):
        cGen = CGenerator(creator,company,disclaimer,cppMode)
        projectDir = os.path.join(path,projectName)
        strPathVsCode = os.path.join(projectDir,".vscode")
        strPathSource = os.path.join(projectDir,"src")

        #
        # Create neccesary paths
        #
        CMakeGenerator.checkCreatePath(projectDir)
        CMakeGenerator.checkCreatePath(strPathVsCode)
        CMakeGenerator.checkCreatePath(strPathSource)

        #
        # Generate CMakeLists File
        #
        CMakeGenerator.genCMakeLists(projectDir,projectName,cpp=cppMode)

        #
        # Copy build scripts
        #
        Template.copyFile("build.bat",projectDir)
        Template.copyFile("build.sh",projectDir)
        Template.copyFile("build.command",projectDir)

        #
        # Copy vscode files
        #
        Template.copyFileReplaceVars(fileName="launch.json",toPath=strPathVsCode,projectName=projectName,creator=creator,company=company,subTemplateDir=".vscode")
        Template.copyFileReplaceVars(fileName="tasks.json",toPath=strPathVsCode,projectName=projectName,creator=creator,company=company,subTemplateDir=".vscode")

        #
        # Generate disclaimer
        #
        CMakeGenerator.genDisclaimer(projectDir,creator,company)

        #
        # Generate readme
        #
        CMakeGenerator.genReadme(projectDir,projectName)

        #
        # Create main file
        #
        cGen.createModule(strPathSource,"Main","Main File")
