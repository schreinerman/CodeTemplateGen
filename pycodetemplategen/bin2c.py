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

class Bin2C(object):
    def __init__(self):
        self.initDone = True

    @staticmethod
    def binFileToCFile(self,binFile,cFileOut):
        tmp = self.binfileToC(binFile)
        cFile = open(cFileOut, 'w')
        cFile.write(tmp)
        cFile.close()

    @staticmethod
    def binfileToC(self,fileName):
        with open(fileName, 'rb') as f:
            bytearray = f.read()
            return self.bin2C(bytearray,fileName)

    @staticmethod
    def bin2C(self,bytearray,fileName="FileName"):
        tmp = ""
        fileNameConverted = Path(fileName).name.replace(".","_")
        tmp = "#if !defined(__" + fileNameConverted.upper() +  "__)\r\n"
        tmp += "#define __" + fileNameConverted.upper() +  "__\r\n"
        tmp += "const char* bin" + fileNameConverted + "[" + str(len(bytearray)) + "] = {\r\n"
        count = 0
        for byte in bytearray:
            count += 1
            tmp += hex(byte) + ","
            # every 20 entries, do a line break
            if count % 20 == 0:
                tmp += "\r\n"
        tmp += "};\r\n"
        tmp += "#endif //!defined(__" + fileNameConverted.upper() +  "__)\r\n"
        return tmp


