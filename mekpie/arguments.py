# Qualified local imports
import mekpie.messages as messages
import mekpie.debug    as debug

# Local imports
from .definitions import Options
from .util import (
    car,
    shift,
    empty,
    panic,
    tab,
    underline,
)
from .create import (
    command_new,
    command_init,
)
from .compiler import (
    command_clean,
    command_build,
    command_run,
    command_debug,
    command_test,
)

def command_help(options):
    print(messages.usage)

def command_version(options):
    print(messages.version)

def default_options():
    return Options(
        quiet       = False,
        verbose     = False,
        release     = False,
        developer   = False,
        changedir   = False,
        debug       = False,
        command     = None,
        subargs     = [],
        programargs = [],
    )._asdict()

def available_options():
    return [
        flag('quiet',               ['-q', '--quiet']),
        flag('verbose',             ['-v', '--verbose']),
        flag('release',             ['-r', '--release']),
        flag('developer',           ['-d', '--developer']),
        arg('changedir',         2, ['-c', '--changedir']),
        arg('programargs',     100, ['--']),
        command(command_help,    1, ['-h', '--help', 'help']),
        command(command_version, 1, ['-V', '--version', 'version']),
        command(command_new,     2, ['new']),
        command(command_init,    1, ['init']),
        command(command_clean,   1, ['clean']),
        command(command_build,   1, ['build']),
        command(command_run,     1, ['run']),
        command(command_test,    2, ['test']),
        command(command_debug,   1, ['debug']),
    ]

def pre_config_commands():
    return [
        command_new,
        command_init,
        command_help,
        command_version,
    ]

def parse(args):
    options = default_options()
    while not empty(args):
        for option in available_options():
            if option(args, options):
                break
        else:
            argument_error(messages.unknown_argument, car(args))
    return Options(**options)

def add_debug(options):
    options['debug'] = options['command'] == command_debug

def option(aliases, n, handler):
    def parse_option(args, options):
        if car(args) in aliases:
            handler(args[1:n], options)
            shift(args, n)
            return True
    return parse_option

def flag(name, aliases):
    return option(
        aliases = aliases, 
        n       = 1, 
        handler = lambda _, options : add_arg(name, True, options),
    )

def arg(name, n, aliases):
    return option(
        aliases = aliases, 
        n       = n, 
        handler = lambda args, options : add_arg(name, args, options),
    )

def command(command, n, aliases):
    return option(
        aliases = aliases, 
        n       = n, 
        handler = lambda args, options : add_command(command, args, options),
    )

def add_arg(name, arg, options):
    if options[name]:
        argument_error(messages.repeated_option.format(name), name)
    else:
        options[name] = arg

def add_command(command, subargs, options):
    if options['command']:
        argument_error(messages.too_many_arguments, command)
    else:
        options['command'] = command
        options['subargs'] = subargs

def argument_error(message, arg):
    args = ['mekpie'] + debug.args
    panic(f'{message}\n{tab(underline(arg, args))}')