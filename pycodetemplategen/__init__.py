
#!/usr/bin/env python3

import argparse
import inspect
import os
import sys
import time
import shlex

__version__ = "1.0"

from pycodetemplategen.util import (
    FatalError
)

# Make Py2's str equivalent to Py3's
str = type('')

from pycodetemplategen.cgenerator import CGenerator
from pycodetemplategen.text2c import Text2C
from pycodetemplategen.bin2c import Bin2C
from pycodetemplategen.template import Template
from pycodetemplategen.commands import Commands

parser = argparse.ArgumentParser(
        description="codetemplategen.py v%s - CodeTemplate Generator Utility"
        % __version__,
        prog="codetemplategen",
    )

def cmd_print_help(args):
    parser.print_help()
    sys.exit(1)

def expand_file_arguments(argv):
    """
    Any argument starting with "@" gets replaced with all values read from a text file.
    Text file arguments can be split by newline or by space.
    Values are added "as-is", as if they were specified in this order
    on the command line.
    """
    new_args = []
    expanded = False
    for arg in argv:
        if arg.startswith("@"):
            expanded = True
            with open(arg[1:], "r") as f:
                for line in f.readlines():
                    new_args += shlex.split(line)
        else:
            new_args.append(arg)
    if expanded:
        print("codetemplategen %s" % (" ".join(new_args[1:])))
        return new_args
    return argv

def main(argv=None):
    """
    Main function for codetemplategen tool
    argv - Optional override for default arguments parsing (that uses sys.argv),
    can be a list of custom arguments as strings. Arguments and their values
    need to be added as individual items to the list
    """

    parser.add_argument(
        "--type",
        "-t",
        help="Optional type of project",
        default="c-module",
        choices=[
            "c-module",
            "cpp-module",
            "cmake-project",
            "bin2c",
            "text2c"
        ],
    )

    parser.add_argument(
        "--cpp",
        "-cpp",
        help="Optional generate cpp extension instead of c",
        action="store_true"
    )

    parser.add_argument(
        "--text2c",
        "-txt2c",
        action="store_true",
        help="execute text to C"
    )

    parser.add_argument(
        "--bin2c",
        "-bin2c",
        action="store_true",
        help="execute bin to C"
    )

    parser.add_argument(
        "--cmake",
        "-cmake",
        action="store_true",
        help="execute bin to C"
    )



    parser.add_argument(
        "--creator",
        "-c",
        #required=True,
        type=str,
        help="Name of creator"
    )

    parser.add_argument(
        "--modulename",
        "-m",
        #required=True,
        type=str,
        help="Name of module without special characters in CamelCase"
    )

    parser.add_argument(
        "--description",
        "-d",
        #required=True,
        type=str,
        help="Module description"
    )

    parser.add_argument(
        "--outputfile",
        "-f",
        #required=True,
        type=str,
        help="output file, required for bin2c / text2c"
    )

    parser.add_argument(
        "--inputfile",
        "-i",
        #required=True,
        type=str,
        help="input file, required for bin2c / text2c"
    )
    

    parser.add_argument(
        "--organisation",
        "--company",
        "-o",
        default="",
        type=str,
        help="optional company / organisation"
    )

    parser.add_argument(
        "--project",
        "-p",
        type=str,
        help="Project name"
    )

    parser.add_argument(
        "--workdir",
        "-w",
        type=str,
        default=os.getcwd(),
        help="Working Directory"
    )

    argv = expand_file_arguments(argv or sys.argv[1:])

    args = parser.parse_args(argv)
    print("codetemplategen.py v%s" % __version__)

    error_happened = False

    execCmd=cmd_print_help

    #print(args)

    os.chdir(args.workdir)

    cmd_type = args.type
    if args.cpp:
        cmd_type = "cpp-project"
    if args.bin2c:
        cmd_type = "bin2c"
    if args.text2c:
        cmd_type = "text2c"
    if args.cmake:
        cmd_type = "cmake-project"
    if args.project:
        cmd_type = "cmake-project"

    if cmd_type == 'c-module' or cmd_type == 'cpp-module':
        if not args.creator:
            print("Type of c-modules needs the creator specified")
            error_happened = True
        if not args.modulename:
            print("Type of c-modules needs the modulename specified")
            error_happened = True
        if not args.description:
            print("Type of c-modules needs the description specified")
            error_happened = True
        execCmd=Commands.cmd_cmodule

    if cmd_type == 'cmake-project':
        if not args.project:
            print("Type of cmake-project needs the project name specified")
            error_happened = True
        execCmd=Commands.cmd_cmakeproject

    if cmd_type == 'text2c':
        if not args.outputfile:
            print("Type of text2c needs an outputfile")
            error_happened = True
        if not args.inputfile:
            print("Type of text2c needs an inputfile")
            error_happened = True
        execCmd=Commands.cmd_text2c

    if cmd_type == 'bin2c':
        if not args.outputfile:
            print("Type of bin2c needs an outputfile")
            error_happened = True
        if not args.inputfile:
            print("Type of bin2c needs an inputfile")
            error_happened = True
        execCmd=Commands.cmd_bin2c

    if error_happened:
        parser.print_help()
        sys.exit(1)

    execCmd(args)

def _main():
    try:
        main()
    except FatalError as e:
        print("\nA fatal error occurred: %s" % e)
        sys.exit(2)


if __name__ == "__main__":
    _main()