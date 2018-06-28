# External Imports
from collections import namedtuple

# Qualified Local Imports
import mekpie.messages as messages

# Local Imports
from .definitions import CompilerFlags
from .util        import panic, flatten

def default_output(path):
    return [f'-o', path]

def default_include(path):
    return [f'-I', path]

def default_libs(lib):
    return [f'-l{lib}']

def default_define(name, definition):
    if definition == True:
        return [f'-D{name}']
    if definition == False:
        return [f'-U{name}']
    else:
        return [f'-D{name}={definition}']

compilers = {
    # Default compiler flags
    'default' : CompilerFlags(
        output       = default_output,
        include      = default_include,
        libs         = default_libs,
        define       = default_define,
        warning      = ['-Wall', '-Wextra'],
        strict       = ['-Werror'],
        assemble     = ['-c'],
        debug        = ['-g'],
        optimization = ['-O'],
        custom       = [],
    ),
    # Compiler flag configuration for clang
    'clang' : 'default',
    # Compiler flag configuration for gcc
    'gcc' : 'default',
}

def derive_flags(config, output, debug, release, assemble):
    return flatten([
        # Config Derived flags
        flatten([get_flags('include', config)(inc)
            for inc in config.includes]),
        flatten([get_flags('libs',    config)(lib)
            for lib in config.libs]),
        flatten([get_flags('define',  config)(name, value)
            for name, value in config.define.items()]),
        # Compiler derived flags
        get_flags('define',       config)('VERSION', f'"{config.version}"'),
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

def aliased(flags):
    return type(flags) == str

def compiler_default_flags(key, config):
    if aliased(compilers[config.cc]):
        return getattr(compilers[compilers[config.cc]], key)
    else:
        return getattr(compilers[config.cc], key)