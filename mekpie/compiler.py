# External imports
from collections import namedtuple
from subprocess  import run
from os.path     import basename, join, abspath

# Qualified local imports
import mekpie.messages as messages

# Local imports
from .util      import (
    panic, 
    car,
    list_files, 
    flatten, 
    filename, 
    remove_contents, 
    empty,
)
from .structure import (
    get_src_path, 
    get_test_path, 
    get_target_debug_path,
    get_target_release_path,
    get_target_build_path,
    get_target_tests_path,
)

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

compilers = {
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
}

def command_clean(options, config):
    remove_contents(get_target_debug_path())
    remove_contents(get_target_release_path())
    remove_contents(get_target_tests_path())

def command_build(options, config):
    add_default_includes(config)
    assemble_main(options, config)
    link(
        target_objects(options.release), 
        get_target(options, config), 
        options, 
        config,
    )

def add_default_includes(config):
    config.includes.append('includes')

def get_target(options, config):
    return join(get_target_build_path(options.release), filename(config.main))

def command_run(options, config):
    command_build(options, config)
    run([get_target(options, config)])

def command_debug(options, config):
    command_build(options, config)
    run([config.dbg, get_target(options, config)])

def command_test(options, config):
    add_default_includes(config)
    assemble_main(options, config)
    assemble_test(options, config)
    for (objects, name) in test_objects(options, config.main):
        output = join(get_target_tests_path(), name)
        link(objects, output, options, config)
        run([output])

def assemble_main(options, config):
    assemble(
        get_units_from(get_src_path(), get_target_build_path(options.release)), 
        options, 
        config
    )

def assemble_test(options, config):
    assemble(
        get_units_from(get_test_path(), get_target_tests_path()), 
        options, 
        config
    )

def target_objects(release):
    return list_files(
        get_target_build_path(release), 
        with_ext='.o',
    )

def test_objects(options, main):
    def not_main(ofile):
        return filename(ofile) != filename(main)
    ofiles  = list(filter(not_main, target_objects(options.release)))
    objects = [
        (ofiles + [ofile], filename(ofile)) 
        for ofile 
        in list_files(get_target_tests_path(), with_ext='.o')
        if not test_name(options) or filename(ofile) == test_name(options)
    ]
    if empty(objects) and not test_name(options):
        panic(messages.no_tests)
    if empty(objects):
        panic(messages.no_tests_with_name.format(test_name(options)))
    return objects

def test_name(options):
    return car(options.subargs)

def get_units_from(path, target):
    return [get_unit(cfile, target) for cfile in list_files(
        path, 
        with_ext='.c', 
        recursive=True
    )]

def get_unit(cfile, target):
    ofile = join(target, basename(cfile).replace('.c', '.o'))
    return (cfile, ofile)

def derive_flags(options, config, assemble=False):
    debug   = options.command == command_debug
    release = options.release
    return CompilerFlags(
        # Config Derived flags
        include = flatten(map(get_flags('include', config), config.includes)),
        libs    = flatten(map(get_flags('libs',    config), config.libs)),
        # Compiler derived flags
        output       = get_flags('output',       config),
        warning      = get_flags('warning',      config),
        strict       = get_flags('strict',       config),
        assemble     = get_flags('assemble',     config) if assemble else [],
        debug        = get_flags('debug',        config) if debug    else [],
        optimization = get_flags('optimization', config) if release  else [],
        custom       = get_flags('custom',       config),
    )

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
    key += '_flags'
    return hasattr(config, key) and getattr(config, key)

def compiler_has_default_flags(config):
    return compilers[config.cc] is not None

def user_flags(key, config):
    return getattr(config, key + '_flags')

def compiler_default_flags(key, config):
    return getattr(compilers[config.cc], key)

def assemble(units, options, config):
    for (cfile, ofile) in units:
        compiler_call(
            cmd    = config.cc,
            inputs = [cfile],
            output = ofile,
            flags  = derive_flags(options, config, assemble=True),
        )

def link(objects, output, options, config):
    compiler_call(
        cmd    = config.cc,
        inputs = objects,
        output = output,
        flags  = derive_flags(options, config),
    )

def compiler_call(cmd, inputs, output, flags):
    run([cmd] + inputs + serialize_flags(flags, output))

def serialize_flags(flags, output):
    return flatten([
        flags.output(output),
        flags.include,
        flags.libs,
        flags.warning,
        flags.strict,
        flags.assemble,
        flags.debug,
        flags.optimization,
        flags.custom,
    ])