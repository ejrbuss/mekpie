# External Imports
from collections import namedtuple

Options = namedtuple('Options', [
    'quiet',       # -q --quiet
    'verbose',     # -v --verbose
    'release',     # -r --release
    'developer',   # -d --developer
    'changedir',   # -c --changedir
    'command',     # new, init, build, run, test, debug
    'debug',       # debug
    'subargs',     # <command args>
    'programargs', # - <program args>
])

Config = namedtuple('Config', [
    'name',     # Project name
    'main',     # Entry point
    'includes', # Header folders
    'libs',     # Libraries to link
    'cc',       # C Compiler Configuration
    'cmd',      # The C Compiler command
    'dbg',      # Debugger
    'flags',    # Custom flags
    'version',  # Version string
    'define',   # A set of preprocessor variables to define/undefined
])

CompilerFlags = namedtuple('CompilerFlags', [
    'output',       # Output flag format function
    'include',      # Include flag format function
    'libs',         # library flag format function
    'define',       # define flag format function
    'warning',      # Enable warnings
    'strict',       # Enable error on warning
    'assemble',     # Flags specific to assembly
    'debug',        # Enable debugging symbols
    'optimization', # Enable optimizations
    'custom',       # Additional custom flags
])

MekpieResult = namedtuple('MekpieResult', [
    'commands',   # An array of commands run
])

Command = namedtuple('Command', [
    'args',       # The arguments passed on the command line
    'sargs',      # Serialized args
    'stdout',     # A string copy of stdout
    'stderr',     # A string copy of stderr
    'returncode', # The command return code
])

DEFAULT_MEKPY='''
# This is a standard configuration file for mekpie

# the name of your project
name = '{}'
# the version of your project
version = '1.0.0'
# the .c file containing `main`
main = '{}'
# any include directories
includes = ['./includes']
# any libraries to load
libs = []
# the c compiler configuration to use (default, gcc, clang, cl)
cc = '{}'
# the c compiler command to use on the command line
cmd = '{}'
# the debugger to use
dbg = 'gdb'
'''

MAIN = '''
#include <stdio.h>
#include <stdlib.h>

int main() {
    puts("Hello, World!");
    return EXIT_SUCCESS;
}
'''.strip()

VERSION = '0.0.1'