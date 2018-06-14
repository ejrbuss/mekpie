# External Imports
from shutil import which
from os     import name

# Qualified local imports
import mekpie.messages as messages

# Local Imports
from .util   import panic, log
from .cflags import compilers
from .runner import lrun

def autodetect_compiler():
    if defined('cc'):
        return get_compiler_config('cc')
    if posix():
        if defined('clang'):
            return get_compiler_config('clang')
        if defined('gcc'):
            return get_compiler_config('gcc')
    if windows():
        if defined('cl'):
            return get_compiler_config('cl')
        if defined('clang'):
            return get_compiler_config('clang')
        if defined('gcc'):
            return get_compiler_config('gcc')
    panic(messages.failed_autodetect)

def get_compiler_config(cmd):
    if (cmd == 'cc'):
        return (disambiguate(), 'cc')
    return (cmd, cmd)

def disambiguate():
    cc = identifier('cc')
    log(cc)
    for (compiler, path)  in log([(compiler, identifier(compiler)) 
        for compiler 
        in compilers.keys()]):
        if cc == path:
            return compiler
    return 'default'

def identifier(cc):
    result = lrun([cc], quiet=True, error=False)
    return result.stderr + result.stdout

def defined(name):
    return which(name) is not None

def posix():
    return name == 'posix'

def windows():
    return name == 'nt'