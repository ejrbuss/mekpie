# Qualified local imports
import mekpie.messages as messages
import mekpie.debug    as debug

# Local imports
from .definitions import Options
from .util import (
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
    command_build,
    command_run,
    command_debug,
    command_test,
)

def command_help(options):
    print(messages.usage)

def command_version(options):
    print(messages.version)

def parse(args):
    options = default_options()
    for arg in args:
        for try_option in default_command_line_options():
            if try_option(arg, options):
                break
        else:
            try_name(arg, options)
    return Options(**options)

def default_options():
    return Options(
        quiet     = False,
        verbose   = False,
        release   = False,
        developer = False,
        changedir = False,
        command   = None,
        name      = '',
    )._asdict()

def default_command_line_options():
    return [add_option(option, aliases) for (option, aliases) in [
        ('quiet',         ['-q', '--quiet']),
        ('verbose',       ['-v', '--verbose']),
        ('release',       ['-r', '--release']),
        ('developer',     ['-d', '--developer']),
        ('changedir',     ['-c', '--changedir']),
        (command_help,    ['-h', '--help', 'help']),
        (command_version, ['-V', '--version', 'version']),
        (command_new,     ['new']),
        (command_init,    ['init']),
        (command_build,   ['build']),
        (command_run,     ['run']),
        (command_test,    ['test']),
        (command_debug,   ['debug']),
    ]]

def pre_config_commands():
    return [
        command_new,
        command_init,
        command_help,
        command_version,
    ]

def add_option(option, aliases):
    def try_option(arg, options):
        if arg in aliases:
            if is_flag(option):
                add_flag(option, options)
            if is_command(option):
                add_command(option, options)
            return True
    return try_option

def is_flag(option):
    return type(option) == str

def is_command(option):
    return callable(option)

def add_flag(flag, options):
    if options[flag]:
        argument_error(messages.repeated_option.format(flag), flag)
    else:
        options[flag] = True

def add_command(command, options):
    if options['command']:
        argument_error(messages.too_many_arguments, command)
    else:
        options['command'] = command

def try_name(arg, options):
    if not options['command']:
        argument_error(messages.unknown_argument, arg)
    if options['name']:
        argument_error(messages.too_many_arguments, arg)
    options['name'] = arg

def argument_error(message, arg):
    args = ['mekpie'] + debug.args
    panic(f'{message}\n{tab(underline(arg, args))}')