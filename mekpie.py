import subprocess
import importlib
import hashlib
import shutil
import json
import sys
import os

# Default Configuration
# ---------------------

cc       = 'gcc'
target   = './bin'
start    = ''
flags    = []
cfiles   = []
includes = []
tests    = []

# Utility Functions
# -----------------

def panic(message):
    sys.stderr.write(f'panic! {message}\n')
    exit()

def files(path):
    if os.path.isfile(path):
        return [path]
    if os.path.isdir(path):
        fs = []
        for f in os.listdir(path):
            fs += files(f)
        return fs
    else:
        panic(f'{path} is not a file!')

def load():
    global chash

    # Read build configuration
    if not os.path.isfile('./build.py'):
        panic('Could not find build file (build.py) in your cwd!')
    with open('./build.py') as f:
        contents = f.read()
        exec(contents, globals())
        chash = hashlib.sha256(contents.encode('utf-8')).hexdigest()

    # Check configuration types
    if type(cc) != str:
        panic('`cc` must be speciifed as a string')
    if type(target) != str:
        panic('`target` must be specified as a string')
    if type(start) != str:
        panic('`start` must be specified as a string')
    if type(flags) != list:
        panic('`flags` must be specified as a list')
    if type(cfiles) != list:
        panic('`cfiles` must be specified as a list')
    if type(includes) != list:
        panic('`includes` must be specified as a list')
    if type(tests) != list:
        panic('`tests` must be specified as a list')

    # Print configuration
    print(
f'''> found config {chash}
    cc       : {cc}
    target   : {target}
    start    : {start}
    flags    : {flags}
    cfiles   : {cfiles}
    includes : {includes}
    tests    : {tests}''')

    # Prepare working directroy
    if not os.path.exists(target):
        print(f'> creating target directory {target}')
        os.mkdir(target)

def build():
    cfiles = files(start) + files(cfiles) + files(test)
    print(cfiles)

def run():
    pass

if __name__ == '__main__':
    print(
r'''
mekpie v0.0.1
> loading...'''
    )
    load()
    build()
    run()


