from os.path import isdir, curdir, join
from os      import mkdir

import mekpie.messages as messages

from .util        import panic, empty
from .config      import read_config
from .definitions import DEFAULT_MEKPY, MAIN
from .structure   import (
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

def action_new(options):
    name = options.name
    check_name(name)
    create_project_directory(name)
    create_mekpy(name)
    create_src(name)
    create_tests(name)
    create_includes(name)
    create_target(name)
    config = read_config(get_mekpy_source(name))

def check_name(name):
    if isdir(name):
        panic(messages.name_cannot_already_exist.format(name))
    if empty(name):
        panic(messages.name_cannot_be_empty)

def create_project_directory(name):
    mkdir(get_project_path(name))

def create_mekpy(name):
    open(get_mekpy_path(name), 'w+').write(get_mekpy_source(name))

def create_src(name):
    mkdir(get_src_path(name))
    open(get_main_path(name, name + '.c'), 'w+').write(get_main_source())

def create_tests(name):
    mkdir(get_test_path(name))

def create_includes(name):
    mkdir(get_includes_path(name))

def create_target(name):
    mkdir(get_target_path(name))
    mkdir(get_target_debug_path(name))
    mkdir(get_target_release_path(name))
    mkdir(get_target_tests_path(name))

def action_init(options):
    panic(f'action_init:\n{options}')

def get_mekpy_source(name):
    return DEFAULT_MEKPY.format(name, name + '.c')

def get_main_source():
    return MAIN