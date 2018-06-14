# External Imports
from collections import namedtuple

# Qualified Local Imports
import mekpie.messages as messages

# Local Imports
from .definitions import CompilerFlags
from .util        import panic, flatten

compilers = {
    # Default compiler flags
    'default' : CompilerFlags(
        output       = lambda path : [f'-o', path],
        include      = lambda path : [f'-I', path],
        libs         = lambda lib : [f'-l{lib}'],
        warning      = ['-Wall', '-Wpedantic', '-Wextra'],
        strict       = ['-Werror'],
        assemble     = ['-c'],
        debug        = ['-g'],
        optimization = ['-O'],
        custom       = [],
    ),
    # Compiler flag configuration for clang
    'clang' : CompilerFlags(
        output       = lambda path : [f'-o', path],
        include      = lambda path : [f'-I', path],
        libs         = lambda lib : [f'-l{lib}'],
        warning      = ['-Wall', '-Wpedantic', '-Wextra'],
        strict       = ['-Werror'],
        assemble     = ['-c'],
        debug        = ['-g'],
        optimization = ['-O'],
        custom       = [],
    ),
    # Compiler flag configuration for gcc
    'gcc' : CompilerFlags(
        output       = lambda path : [f'-o', path],
        include      = lambda path : [f'-I', path],
        libs         = lambda lib : [f'-l{lib}'],
        warning      = ['-Wall', '-Wpedantic', '-Wextra'],
        strict       = ['-Werror'],
        assemble     = ['-c'],
        debug        = ['-g'],
        optimization = ['-O'],
        custom       = [],
    ),
    # Compiler flag configuration for cl
    'cl' : CompilerFlags(
        output       = lambda path : [f'-o', path],
        include      = lambda path : [f'-I', path],
        libs         = lambda lib : [f'-l{lib}'],
        warning      = ['-Wall', '-Wpedantic', '-Wextra'],
        strict       = ['-Werror'],
        assemble     = ['-c'],
        debug        = ['-g'],
        optimization = ['-O'],
        custom       = [],
    ),
}

def derive_flags(config, output, debug, release, assemble):
    return flatten([
        # Config Derived flags
        flatten(map(get_flags('include', config), config.includes)),
        flatten(map(get_flags('libs',    config), config.libs)),
        # Compiler derived flags
        get_flags('output',       config)(output),
        get_flags('warning',      config),
        get_flags('strict',       config),
        get_flags('custom',       config),
        get_flags('debug',        config) if debug    else [],
        get_flags('optimization', config) if release  else [],
        get_flags('assemble',     config) if assemble else [],
    ])

def get_flags(key, config):
    if user_has_overriden_flags(key, config):
        return user_flags(key, config)
    if compiler_has_default_flags(config):
        return compiler_default_flags(key, config)
    panic(messages.compiler_flag_error.format(
        config.cc,
        key,
        key + '_flag = []',
    ))
    
def user_has_overriden_flags(key, config):
    return hasattr(config.flags, key) and getattr(config.flags, key)

def compiler_has_default_flags(config):
    return compilers[config.cc] is not None

def user_flags(key, config):
    return getattr(config.flags, key)

def compiler_default_flags(key, config):
    return getattr(compilers[config.cc], key)