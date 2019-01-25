
# This is a standard configuration file for mekpie

# the name of your project
name = 'test' 
# the .c file containing `main`
main = 'test.c'
# any libraries to load
libs = []
# the c compiler configuration to use (gcc/clang)
cc = 'gcc/clang'
# the c compiler command to use on the command line
cmd = 'clang'
# the debugger to use
dbg = 'lldb'
# additional compiler flags
flags = ['-Wall']

if options.release:
    flags = flags + ['-O']
else:
    flags = flags + ['-g']
