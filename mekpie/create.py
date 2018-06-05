# External imports
from os.path import isdir, curdir, join
from os      import mkdir

# Qualified local imports
import mekpie.messages as messages

# Local imports
from .util        import panic, empty
from .config      import read_config
from .definitions import DEFAULT_MEKPY, MAIN
from .structure   import (
    set_project_path,
    get_project_path,
    get_mekpy_path,
    get_src_path,
    get_main_path,
    get_test_path,
    get_includes_path,
    get_target_path,
    get_target_debug_path,
    get_target_release_path,
    get_target_tests_path,
)

def command_new(options):
    name = options.name
    check_name(name)
    create_project_directory(name)
    create_mekpy(name)
    create_src(name)
    create_tests()
    create_includes()
    create_target()
    read_config(get_mekpy_source(name))

def check_name(name):
    if isdir(name):
        panic(messages.name_cannot_already_exist.format(name))
    if empty(name):
        panic(messages.name_cannot_be_empty)

def create_project_directory(name):
    set_project_path(name)
    mkdir(get_project_path())

def create_mekpy(name):
    open(get_mekpy_path(), 'w+').write(get_mekpy_source(name))

def create_src(name):
    mkdir(get_src_path())
    open(get_main_path(name + '.c'), 'w+').write(get_main_source())

def create_tests():
    mkdir(get_test_path())

def create_includes():
    mkdir(get_includes_path())

def create_target():
    mkdir(get_target_path())
    mkdir(get_target_debug_path())
    mkdir(get_target_release_path())
    mkdir(get_target_tests_path())

def get_mekpy_source(name):
    return DEFAULT_MEKPY.format(name, name + '.c')

def get_main_source():
    return MAIN

def command_init(options):
    name = options.name
    check_name(name)
    create_mekpy(name)
    create_src(name)
    create_tests()
    create_includes()
    create_target()
    read_config(get_mekpy_source(name))
