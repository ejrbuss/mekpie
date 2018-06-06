# External imports
from os.path import join

# Qualified local imports
import mekpie.messages as messages

# Local imports
from .definitions import Config, CompilerFlags
from .util        import panic, tab, check_is_file, check_is_dir, type_name
from .structure   import get_main_path

def read_config(source):
    config_dict = {}
    try:
        exec(source, config_dict)
    except Exception as err:
        panic(messages.error_reading_mekpy.format(tab(str(err))))
    return config_from_dict(config_dict)

def config_from_dict(config_dict):
    return check_config(Config(
        name     = config_dict.get('name',     None),
        main     = config_dict.get('main',     None),
        includes = config_dict.get('includes', ['./includes']),
        libs     = config_dict.get('libs',     []),
        cc       = config_dict.get('cc',       'gcc'),
        dbg      = config_dict.get('dbg',      'gdb'),
        flags    = CompilerFlags(
            output       = config_dict.get('output_flags',       None),
            include      = config_dict.get('include_flags',      None),
            libs         = config_dict.get('libs_flags',         None),
            warning      = config_dict.get('warning_flags',      None), 
            strict       = config_dict.get('strict_flags',       None),
            assemble     = config_dict.get('assemble_flags',     None),
            debug        = config_dict.get('debug_flags',        None),
            optimization = config_dict.get('optimization_flags', None),
            custom       = config_dict.get('custom_flags',       None),
        )
    ))

def check_config(config):
    check_name(config.name)
    check_main(config)
    check_includes(config.includes)
    check_libs(config.libs)
    check_cc(config.cc)
    check_dbg(config.dbg)
    check_flags(config.flags)
    return config

def check_name(name):
    check_type('name', name, str)

def check_main(config):
    check_type('main', config.main, str)
    check_is_file(get_main_path(config.main))

def check_includes(includes):
    check_type('includes', includes, list)
    for directory in includes:
        check_type('includes directory', directory, str)
        check_is_dir(directory)

def check_libs(libs):
    check_type('libs', libs, list)
    for lib in libs:
        check_type('lib', lib, str)

def check_cc(cc):
    check_type('cc', cc, str)

def check_dbg(dbg):
    check_type('dbg', dbg, str)

def check_flags(flags):
    if flags.output:
        check_type('output_flags', flags.output, type(lambda:None))
    if flags.include:
        check_type('include_flags', flags.include, type(lambda:None))
    if flags.libs:
        check_type('libs_flags', flags.libs, type(lambda:None))
    if flags.warning:
        check_type('warning_flags', flags.warning, list)
    if flags.strict:
        check_type('strict_flags', flags.strict, list)
    if flags.assemble:
        check_type('assemble_flags', flags.assemble, list)
    if flags.debug:
        check_type('debug_flags', flags.debug, list)
    if flags.optimization:
        check_type('optimization_flags', flags.optimization, list)
    if flags.custom:
        check_type('custom_flags', flags.custom, list)

def check_type(name, value, expected_type):
    if type(value) != expected_type:
        panic(messages.type_error.format(
            name,
            expected_type.__name__,
            type_name(value),
            tab(get_description(name))
        ))

def get_description(name):
    return {
        'name'               : '`name` specifies the name of the project',
        'main'               : '`main` specifies the .c file continaing `main`',
        'includes'           : '`includes` specifies any additional include directories',
        'libs'               : '`libs` speicfies and libraries to load',
        'cc'                 : '`cc` specifies the c compiler to use',
        'dbg'                : '`dbg` specifies the debugger to use',
        'output_flags'       : '`output_flags` overrides the compiler flags for output',
        'include_flags'      : '`include_flags` overrides the compiler flags for include directories',
        'libs_flags'         : '`libs_flags` overrides the compiler flags for libraries',
        'warning_flags'      : '`warning_flags` overrides the compiler flags for warnings',
        'strict_flags'       : '`strict_flags` overrides the compiler flags for strict warnings',
        'assemble_flags'     : '`assemble_flags` overrides the compiler flags for assembly',
        'debug_flags'        : '`debug_flags` overrides the compiler flags for debugging symbols',
        'optimization_flags' : '`optimization_flags` overrides the compiler flags for optimizations',
        'custom_flags'       : '`custom_flags` specifies additional compiler flags',
    }[name]

def config_path(project_directory):
    return check_is_file(join(project_directory, 'mek.py'))