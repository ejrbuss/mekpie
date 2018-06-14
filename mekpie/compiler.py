# External imports
from collections import namedtuple
from os.path     import basename, join, abspath
from sys         import stdout, stderr

# Qualified local imports
import mekpie.messages as messages

# Local imports
from .runner    import lrun
from .cflags    import derive_flags
from .util      import (
    panic, 
    log,
    car,
    list_files, 
    flatten, 
    tab,
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

def command_clean(options, config):
    remove_contents(get_target_debug_path())
    remove_contents(get_target_release_path())
    remove_contents(get_target_tests_path())

def command_build(options, config):
    assemble_main(options, config)
    link(
        target_objects(options.release), 
        get_target(options, config), 
        options,
        config,
    )

def command_run(options, config):
    command_build(options, config)
    lrun([get_target(options, config)] + options.programargs)

def command_debug(options, config):
    command_build(options, config)
    lrun([config.dbg, get_target(options, config)])

def command_test(options, config):
    assemble_main(options, config)
    assemble_test(options, config)
    for (objects, name) in test_objects(options, config.main):
        output = join(get_target_tests_path(), name)
        link(objects, output, options, config)
        lrun([output])

def get_target(options, config):
    return join(get_target_build_path(options.release), filename(config.main))

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

def assemble_main(options, config):
    assemble(
        get_units_from(get_src_path(), get_target_build_path(options.release)), 
        options,
        config,
    )

def assemble_test(options, config):
    assemble(
        get_units_from(get_test_path(), get_target_tests_path()), 
        options,
        config,
    )

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

def assemble(units, options, config):
    for (cfile, ofile) in units:
        compiler_call(
            options = options,
            cmd     = config.cc,
            inputs  = [cfile],
            output  = ofile,
            flags   = derive_flags(
                config   = config, 
                output   = ofile, 
                debug    = options.debug, 
                release  = options.release, 
                assemble = True,
            )
        )

def link(objects, output, options, config):
    compiler_call(
        options = options,
        cmd     = config.cc,
        inputs  = objects,
        output  = output,
        flags   = derive_flags(
            config   = config, 
            output   = output, 
            debug    = options.debug, 
            release  = options.release, 
            assemble = False,
        )
    )

def compiler_call(options, cmd, inputs, output, flags):
    proc = lrun([cmd] + inputs + flags, quiet=True)
    if proc.returncode != 0:
        panic(None if options.quiet else messages.failed_compiler_call.format(
            proc.sargs, 
            tab(proc.stderr)
        ))
