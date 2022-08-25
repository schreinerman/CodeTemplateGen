
str = type('')
import os
import datetime
import threading
import warnings
import ctypes as ct
from pathlib import Path

from pycodetemplategen.cgenerator import CGenerator
from pycodetemplategen.cmakegenerator import CMakeGenerator
from pycodetemplategen.text2c import Text2C
from pycodetemplategen.bin2c import Bin2C
from pycodetemplategen.template import Template

class Commands:
    @staticmethod
    def cmd_cmodule(args):
        cGen = CGenerator(creator=args.creator,company=args.organisation,cppMode=args.cpp)
        cGen.createModule(os.getcwd(),moduleName=args.modulename,moduleDescription=args.description)

    @staticmethod
    def cmd_cmakeproject(args):
        CMakeGenerator.createProject(path=os.getcwd(),projectName=args.project,creator=args.creator,description=args.description,company=args.organisation,cppMode=args.cpp)

    @staticmethod
    def cmd_bin2c(args):
        """
        Do nothing
        """

    @staticmethod
    def cmd_text2c(args):
        """
        Do nothing
        """