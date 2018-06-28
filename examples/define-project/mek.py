
# This is a standard configuration file for mekpie

# the name of your project
name = 'define-project'
# the version of your project
version = '1.0.0'
# the .c file containing `main`
main = 'define-project.c'
# any include directories
includes = ['./includes']
# any libraries to load
libs = []
# the c compiler configuration to use (default, gcc, clang, cl)
cc = 'gcc'
# the c compiler command to use on the command line
cmd = 'gcc'
# the debugger to use
dbg = 'gdb'
# you can define names and undefine names like so
define = {
    'RELEASE' : False,     # #undef  RELEASE
    'DEBUG'   : True,      # #define DEBUG
    'SECRET'  : '1245154', # #define SECRET 1245154
}
