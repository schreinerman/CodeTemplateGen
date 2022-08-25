# CodeTemplateGen

Build
=====

Python
------
1. Install Python3 (if not yet installed)
2. execute python3 setup.py install in the root folder




Compiling C-Program Windows
---------------------------
1. Download and Install MinGW from https://sourceforge.net/projects/mingw/
2. Download & Install cmake from cmake.org
3. Execute build.bat

Compiling C-Program Linux
-------------------------
1. Install cmake: `sudo apt-get install cmake`
2. Run build.sh
2. Install via `cd build && sudo make install`

Compiling C-Program macOS
-------------------------
1. Install cmake: `brew install cmake`
2. Run build.command
2. Install via `cd build && sudo make install`

````
usage:
codetemplategen -c Joe -m MyModule -d "This is my module"
or as python variant: codetemplategen.py -c Joe -m MyModule -d "This is my module"

-c name
   name = Name of creator

-m modulename
   modulename = Name of module without special characters in CamelCase

-d description
   description = Description

[-o organisation]
   optional company / organisation

[-cpp]
   optional generate cpp extension

[-p project_name]
   optional generate project
````