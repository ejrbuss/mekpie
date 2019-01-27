from time               import time
from os.path            import join
from collections        import namedtuple
from concurrent.futures import ThreadPoolExecutor

import mekpie.messages as messages

from .runner    import lrun
from .util      import (
    smv,
    panic,
    clamp,
    car, 
    cdr,
    list_files, 
    list_all_dirs,
    remove_contents, 
    filename, 
)
from .structure import (
    get_project_path,
    get_test_path,
    get_target_path,
    get_target_debug_path,
    get_target_release_path,
    get_main_path,
    get_src_path,
    get_includes_path,
)

max_threads = 32

def command_clean(cfg):
    remove_contents(get_target_debug_path())
    remove_contents(get_target_release_path())
    if not cfg.options.quiet:
        print(messages.clean.strip())

def command_build(cfg):
    command_clean(cfg)
    start   = time()
    cfg.includes   = get_includes_paths()
    cfg.targetpath = lambda path : get_bin_path(cfg, path)
    cfg.once       = cfg.cc.once(cfg)
    
    objects = compile_objects(cfg)
    exes    = link_exes(cfg, objects)

    if not cfg.options.quiet:
        print(messages.build_succeeded.format(time() - start).strip())

    return exes

def compile_objects(cfg):
    sources = get_sources(cfg)
    runset  = []
    cfg.run = lambda args : lrun(args, 
        quiet  = cfg.options.quiet, 
        error  = False, 
        runset = runset,
    ) 
    with ThreadPoolExecutor(max_workers=clamp(len(sources), 1, max_threads)) as e:
        objects = e.map(lambda source: cfg.cc.compile(cfg, source), sources)
    if not all(runset):
        exit(1)
    return list(objects)

def link_exes(cfg, objects):
    mains   = [get_main_path(cfg.main), *list_files(get_test_path(), with_ext='.c')]
    runset  = []
    cfg.run = lambda args : lrun(args, 
        quiet  = True, 
        error  = False, 
        runset = runset,
    ) 
    with ThreadPoolExecutor(max_workers=clamp(len(mains), 1, max_threads)) as e:
        exes = e.map(lambda main: cfg.cc.link(cfg, main, objects), mains)
    if not all(runset):
        cfg.run = lambda args: lrun(args, cfg.options.quiet)
        for main in mains:
            cfg.cc.link(cfg, main, objects)
    return list(exes)

def command_run(cfg):
    exes = command_build(cfg)
    exe  = car(exes)
    cfg.run = lambda args: lrun(args, cfg.options.quiet)
    cfg.cc.run(cfg, exe)

def command_debug(cfg):
    if cfg.options.release:
        panic(messages.release_debug)
    exes = command_build(cfg)
    exe  = car(exes)
    cfg.run = lambda args: lrun(args, cfg.options.quiet)
    cfg.cc.debug(cfg, exe)

def command_test(cfg):
    exes  = command_build(cfg)
    tests = cdr(exes) 
    cfg.run = lambda args: lrun(args, cfg.options.quiet)
    for test in tests:
        if len(cfg.options.commandargs) == 0 or any(name in test for name in cfg.options.commandargs):
            cfg.cc.run(cfg, test)

def command_dist(cfg):
    exes = command_build(cfg)
    exe  = car(exes)
    smv(exe, join(get_project_path(), cfg.name))

def get_bin_path(cfg, path):
    root = get_target_release_path() if cfg.options.release else get_target_debug_path()
    return join(root, filename(path))

def get_sources(cfg):
    sources = list_files(get_src_path(), with_ext='.c')
    sources.remove(get_main_path(cfg.main))
    return sources

def get_includes_paths():
    includes = get_includes_path()
    return [includes] + list_all_dirs(includes)