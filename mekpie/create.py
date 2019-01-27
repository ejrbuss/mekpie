from os.path import isdir, curdir, join
from os      import chdir
from os.path import basename, abspath, exists

import mekpie.messages as messages

from .util         import panic, empty, car, smkdir, exec_str
from .config       import config_from_str
from .cli          import cli_config, ask, tell
from .definitions  import Config, DEFAULT_MEKPY
from .cc_gcc_clang import gcc_clang, config_gcc_clang
from .structure    import (
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
)

@cli_config('mekpie')
def config_mekpie(options):
    name = ask(messages.mekpie_config_name,
        default   = car(options.commandargs),
        validator = lambda s : not empty(s),
    )
    tell(messages.compiler_configs)
    cc = ask(messages.mekpie_config_cc,
        default = 'gcc_clang',
        options = ['gcc_clang'],
    )
    if cc == 'gcc_clang':
        cc = config_gcc_clang()
    return name, cc

def command_new(options):
    name, cc = config_mekpie(options)
    check_name(name)
    create_project_directory(name)
    create_mekpy(name, cc)
    create_src(name, cc)
    create_tests()
    create_includes()
    create_target()
    config_from_str(options, get_mekpy_source(name, cc))
    print(messages.created.format(name).strip())

def command_init(options):
    if not car(options.commandargs):
        options.commandargs[0] = basename(abspath(curdir))
    name, cc = config_mekpie(options)
    check_name(name)
    create_mekpy(name, cc)
    create_src(name, cc)
    create_tests()
    create_includes()
    create_target()
    config_from_str(options, get_mekpy_source(name, cc))
    print(messages.initialized.format(name).strip())

def check_name(name):
    if not name:
        panic(messages.name_cannot_be_empty)
    if isdir(name):
        panic(messages.name_cannot_already_exist.format(name))

def create_project_directory(name):
    set_project_path(name)
    smkdir(get_project_path())

def create_mekpy(name, cc):
    if not exists(get_mekpy_path()):
        with open(get_mekpy_path(), 'w+') as rsc:
            rsc.write(get_mekpy_source(name, cc))

def create_src(name, cc):
    smkdir(get_src_path())
    if not exists(get_main_path(name + '.c')):
        with open(get_main_path(name + '.c'), 'w+') as rsc:
            rsc.write(cc.csource)

def create_tests():
    smkdir(get_test_path())

def create_includes():
    smkdir(get_includes_path())

def create_target():
    smkdir(get_target_path())
    smkdir(get_target_release_path())
    smkdir(get_target_debug_path())

def get_mekpy_source(name, cc):
    return DEFAULT_MEKPY.format(
        name, 
        name + '.c', 
        str(cc.ccsource),
        str(cc.releaseflags),
        str(cc.debugflags),
    )