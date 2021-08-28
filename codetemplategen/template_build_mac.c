const char* strBuildMac = 
"#!/bin/sh\n"
"SCRIPTPATH=\"$( cd -- \"$(dirname \"$0\")\" >/dev/null 2>&1 ; pwd -P )\"\n"
"cd $SCRIPTPATH\n"
"mkdir -p build\n"
"cd build\n"
"cmake ..\n"
"make\n";
