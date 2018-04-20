# External imports
from os.path import join, basename, abspath
from os      import curdir
from sys     import exc_info

# Qualified local imports
import mekpie.messages as messages

# Local imports
from .definitions import Config
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
        name     = config_dict['name'],
        main     = config_dict['main'],
        includes = config_dict['includes'],
        libs     = config_dict['libs'],
        cc       = config_dict['cc'],
        dbg      = config_dict['dbg'],
    ))

def check_config(config):
    check_name(config.name)
    check_main(config)
    check_includes(config.includes)
    check_libs(config.libs)
    check_cc(config.cc)
    check_dbg(config.dbg)
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
        check_is_dir(directroy)

def check_libs(libs):
    check_type('libs', libs, list)
    for lib in libs:
        check_type('lib', lib, str)

def check_cc(cc):
    check_type('cc', cc, str)

def check_dbg(dbg):
    check_type('dbg', dbg, str)

def check_type(name, value, expected_type):
    if type(value) != expected_type:
        panic(messages.format(
            name,
            expected_type.__name__,
            type_name(value),
            tab(get_description(name))
        ))

def get_description(name):
    return {
        'name'     : '`name` specifies the name of the project',
        'main'     : '`main` specifies the .c file continaing `main`',
        'includes' : '`includes` specifies any additional include directories',
        'libs'     : '`libs` speicfies and libraries to load',
        'cc'       : '`cc` specifies the c compiler to use',
        'dbg'      : '`dbg` specifies the debugger to use'
    }[name]

def config_path(project_directory):
    return check_is_file(join(project_directory, 'mek.py'))