
# This is a standard configuration file for mekpie

# the name of your project
name = 'test' 
# the .c file containing `main`
main = 'test.c'
# the c compiler configuration to use (gcc_clang, avr_gcc, or emscripten)
cc = avr_gcc(hardware='atmega2560', programmer='wiring', baud='115200')
# any libraries to load
libs = []
# additional compiler flags
flags = ['-Wall']

if options.release:
    flags += ['-O']
else:
    flags += ['-g']
