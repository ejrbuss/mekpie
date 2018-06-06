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
    'cc',       # C Compiler
    'dbg',      # Debugger
    'flags',    # Custom flags
])

CompilerFlags = namedtuple('CompilerFlags', [
    'output',       # Output flag format
    'include',      # Include flag format
    'libs',         # library flag format
    'warning',      # Enable warnings
    'strict',       # Enable error on warning
    'assemble',     # Flags specific to assembly
    'debug',        # Enable debugging symbols
    'optimization', # Enable optimizations
    'custom',       # Additional custom flags
])

DEFAULT_MEKPY='''
# This is a standard configuration file for mekpie

# the name of the project
name = '{}'
# the .c file containing `main`
main = '{}'
# any include directories
includes = ['./includes']
# any libraries to load
libs = []
# the c copmiler to use
cc = 'gcc'
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
