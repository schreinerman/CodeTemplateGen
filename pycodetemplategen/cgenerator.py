from __future__ import (
    unicode_literals,
    print_function,
    division,
    absolute_import,
    )

# Make Py2's str and range equivalent to Py3's
str = type('')

import os
import datetime
import threading
import warnings
import ctypes as ct
from pathlib import Path
from pycodetemplategen.template import Template

comment_start= """/**
 *******************************************************************************
 **
"""
comment_end= """ **
 *******************************************************************************
 */        

"""      

standard_disclaimer=Template.readFile("DISCLAIMER.md")

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class CGenerator(object):
    def __init__(self,creator,company="",disclaimer=standard_disclaimer,cppMode=False):
        self.creator = creator
        self.company = company
        self.disclaimer = disclaimer
        self.cppMode = cppMode
        self.initDone = True
    
    def generateMultilineComment(self,string):
        tmp = comment_start
        stringLines = string.splitlines()
        for line in stringLines:
            tmp += " ** " + line + "\r\n"
        tmp += comment_end
        return tmp

    def generateDoxyFunction(self,brief,parameters):
        tmp = "\\brief " + brief + "\r\n"
        for parameter in parameters:
            print(parameter)
            tmp += "\r\n\\param " + parameter.name + "  " + parameter.description
        return self.generateMultilineComment(tmp)

    def generatePublicFunction(self,moduleName,funcReturnType,funcName,brief,parameters):
        tmp = self.generateDoxyFunction(brief,parameters)
        tmp += funcReturnType + " " + moduleName + "_" + funcName + "("
        firstEntry = False
        for parameter in parameters:
            if firstEntry is False:
                firstEntry = True
            else:
                tmp += ", "
            tmp += parameter.type + " " + parameter.name
        tmp += ")\r\n"
        tmp += "{\r\n\r\n"
        tmp += "}\r\n\r\n"
        return tmp

    def generatePublicFunctionPrototype(self,moduleName,funcReturnType,funcName,brief,parameters):
        tmp = funcReturnType + " " + moduleName + "_" + funcName + "("
        firstEntry = False
        for parameter in parameters:
            if firstEntry is False:
                firstEntry = True
            else:
                tmp += ", "
            tmp += parameter.type + " " + parameter.name
        tmp += ");\r\n"
        return tmp

    def generateStaticFunction(self,funcReturnType,funcName,brief,parameters):
        tmp = self.generateDoxyFunction(brief,parameters)
        tmp += "static " + funcReturnType + " " + funcName + "("
        firstEntry = False
        for parameter in parameters:
            if firstEntry is False:
                firstEntry = True
            else:
                tmp += ", "
            tmp += parameter.type + " " + parameter.name
        tmp += ")\r\n"
        tmp += "{\r\n\r\n"
        tmp += "}\r\n\r\n"
        return tmp

    def generateStaticFunctionPrototype(self,funcReturnType,funcName,brief,parameters):
        tmp = "static " + funcReturnType + " " + funcName + "("
        firstEntry = False
        for parameter in parameters:
            if firstEntry is False:
                firstEntry = True
            else:
                tmp += ", "
            tmp += parameter.type + " " + parameter.name
        tmp += ");\r\n"
        return tmp

    def generateHeader(self):
        tmp = "Created by " + self.creator + "\r\n"
        tmp += "\r\n"
        tmp += "Copyright © " + str(datetime.datetime.now().year) + " " + self.company + ". All rights reserved.\r\n"
        tmp += self.disclaimer
        return self.generateMultilineComment(tmp)

    def generateFileHistory(self,fileName,moduleName,moduleDescription):
        tmp = "\\file " + Path(fileName).name.lower() + "\r\n\r\n";
        tmp += moduleDescription + "\r\n"
        tmp += "A detailed description is available at\r\n"
        tmp += "@link " + moduleName + "Group file description @endlink\r\n\r\n"
        tmp += "History:\r\n"
        tmp += "- " + datetime.datetime.now().strftime("%Y-%m-%d") + " 1.00  " + self.creator + "\r\n"
        return self.generateMultilineComment(tmp)

    def generateHFile(self,moduleName,moduleDescription):
        tmp = self.generateHeader()
        if self.cppMode:  
            tmp += self.generateFileHistory(moduleName.lower() + ".hpp",moduleName,moduleDescription)
        else:
            tmp += self.generateFileHistory(moduleName.lower() + ".h",moduleName,moduleDescription)

       
        tmp += "#if !defined(__" + moduleName.upper() + "_H__)\r\n"
        tmp += "#define __" + moduleName.upper() + "_H__\r\n\r\n"
    
        tmp += "/* C binding of definitions if building with C++ compiler */\r\n"
        tmp += "#ifdef __cplusplus\r\n"
        tmp += "extern \"C\"\r\n"
        tmp += "{\r\n"
        tmp += "#endif\r\n\r\n"
        tmp += self.generateMultilineComment("\\defgroup " + moduleName + "Group " + moduleDescription + "\r\n\r\nProvided functions of " + moduleName + ":\r\n\r\n\r\n")
        tmp += "//@{\r\n\r\n"

        tmp += self.generateMultilineComment("(Global) Include files")

        tmp += "#include <stdint.h>\r\n"
        tmp += "#include <stdbool.h>\r\n\r\n"

        tmp += self.generateMultilineComment("Global pre-processor symbols/macros ('#define') \r\n")
        tmp += self.generateMultilineComment("Global type definitions ('typedef') \r\n")
    
        if moduleName.lower() != "main":
            tmp += "typedef struct stc_" + moduleName.lower() + "_handle\r\n"
            tmp += "{\r\n"
            tmp += "    uint8_t u8Dummy;\r\n"
            tmp += "} stc_" + moduleName.lower() + "_handle_t;\r\n\r\n"
    
        
        tmp += self.generateMultilineComment("Global variable declarations ('extern', definition in C source)\r\n")

        tmp += self.generateMultilineComment("Global function prototypes ('extern', definition in C source) \r\n")
        
        if moduleName.lower() != "main":
            parms = [Struct(**{"name":"pstcHandle","type":"stc_" + moduleName.lower() + "_handle_t*","description":"Initialization of handle"})]
            tmp += self.generatePublicFunctionPrototype(moduleName,"int","Init","Initialization Function",parms)

            parms = [Struct(**{"name":"pstcHandle","type":"stc_" + moduleName.lower() + "_handle_t*","description":"Deinitialization of handle"})]
            tmp += self.generatePublicFunctionPrototype(moduleName,"int","Deinit","Deinitialization Function",parms)

        
        tmp += "//@} // " + moduleName + "Group\r\n\r\n"
        
        tmp += "#ifdef __cplusplus\r\n"
        tmp += "}\r\n"
        tmp += "#endif\r\n\r\n"

        tmp += "#endif /* __%s_H__ */\r\n\r\n"
        
        tmp += self.generateMultilineComment("EOF (not truncated)")
        return tmp

    def generateCFile(self,moduleName,moduleDescription):
        tmp = self.generateHeader()
        if self.cppMode:  
            tmp += self.generateFileHistory(moduleName.lower() + ".cpp",moduleName,moduleDescription)
            tmp += "#define __" + moduleName.upper() + "_CPP__\r\n\r\n"
        else:
            tmp += self.generateFileHistory(moduleName.lower() + ".c",moduleName,moduleDescription)
            tmp += "#define __" + moduleName.upper() + "_C__\r\n\r\n"
        
        

        tmp += self.generateMultilineComment("Include files")

        if moduleName.lower() == "main":
            tmp += "#include <stdio.h>\r\n"
            tmp += "#include <stdlib.h>\r\n"
        tmp += "#include <string.h> //required also for memset, memcpy, etc.\r\n"
        tmp += "#include <stdint.h>\r\n"
        tmp += "#include <stdbool.h>\r\n"
        tmp += "#include \"" + moduleName.lower() + ".h\"\r\n\r\n"

        tmp += self.generateMultilineComment("Local pre-processor symbols/macros ('#define')")

        tmp += self.generateMultilineComment("Global variable definitions (declared in header file with 'extern')")

        tmp += self.generateMultilineComment("Local type definitions ('typedef')")

        tmp += self.generateMultilineComment("Local variable definitions ('static')")

        tmp += self.generateMultilineComment("Local function prototypes ('static')")

        tmp += self.generateMultilineComment("Function implementation - global ('extern') and local ('static')")
        
        if moduleName.lower() == "main":
            tmp += "int main(int argc, const char * argv[])\r\n"
            tmp += "{\r\n"
            tmp += "    \r\n"
            tmp += "    //add you initialization here...\r\n"
            tmp += "    \r\n"
            tmp += "    //main loop\r\n"
            tmp += "    while(1)\r\n"
            tmp += "    {\r\n"
            tmp += "        //add your looping code here...\r\n"
            tmp += "    }\r\n"
            tmp += "}\r\n\r\n"
        else:
            parms = [Struct(**{"name":"pstcHandle","type":"stc_" + moduleName.lower() + "_handle_t*","description":"Initialization of handle"})]
            tmp += self.generatePublicFunction(moduleName,"int","Init","Initialization Function",parms)

            parms = [Struct(**{"name":"pstcHandle","type":"stc_" + moduleName.lower() + "_handle_t*","description":"Deinitialization of handle"})]
            tmp += self.generatePublicFunction(moduleName,"int","Deinit","Deinitialization Function",parms)

        tmp += self.generateMultilineComment("EOF (not truncated)")
        return tmp

    def createModule(self,path,moduleName,moduleDescription):
        if self.cppMode:  
            cFile = os.path.join(path, moduleName.lower() + ".cpp")
            hFile = os.path.join(path, moduleName.lower() + ".h")
        else:
            cFile = os.path.join(path, moduleName.lower() + ".c")
            hFile = os.path.join(path, moduleName.lower() + ".h")

        cFileHandle = open(cFile, 'w')
        cFileHandle.write(self.generateCFile(moduleName,moduleDescription))
        cFileHandle.close()

        hFileHandle = open(hFile, 'w')
        hFileHandle.write(self.generateHFile(moduleName,moduleDescription))
        hFileHandle.close()