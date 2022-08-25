from __future__ import (
    unicode_literals,
    print_function,
    division,
    absolute_import,
    )

# Make Py2's str and range equivalent to Py3's
str = type('')

import datetime
import threading
import warnings
from pathlib import Path
import ctypes as ct

class Text2C(object):
    def __init__(self):
        self.initDone = True

    @staticmethod
    def textfileToCFile(self,textFile,cFileOut):
        tmp = self.textfileToC(textFile)
        cFile = open(cFileOut, 'w')
        cFile.write(tmp)
        cFile.close()
        
    @staticmethod
    def textfileToC(self,fileName):
        textFile = open(fileName, 'r')
        stringLines = textFile.readlines()
        textFile.close()
        return self.stringLinesToC(stringLines,fileName)

    @staticmethod
    def stringLinesToC(self,stringLines,fileName="FileName"):
        fileNameConverted = Path(fileName).name.replace(".","_")
        tmp = "#if !defined(__" + fileNameConverted.upper() +  "__)\r\n"
        tmp += "#define __" + fileNameConverted.upper() +  "__\r\n"
        tmp += "const char* str" + fileNameConverted + " = \r\n"
        for line in stringLines:
            tmp += "\""
            line = line.replace("\r","")
            line = line.replace("\n","")
            line = line.replace("\\","\\\\")
            line = line.replace("%","\\%")
            line = line.replace("\"","\\\"")
            
            tmp += line
            tmp += "\\r\\n\"\r\n"
        tmp += ";\r\n"
        tmp += "#endif //!defined(__" + fileNameConverted.upper() +  "__)\r\n"
        return tmp

    @staticmethod
    def stringToC(self,string,fileName="FileName"):
        stringLines = string.splitlines()
        return self.stringLinesToC(stringLines,fileName)
