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
    action_new,
    action_init,
)
from .compiler import (
    action_build,
    action_run,
    action_debug,
    action_test,
)

def action_help(options):
    print(messages.usage)

def action_version(options):
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
        action    = None,
        name      = '',
    )._asdict()

def default_command_line_options():
    return [add_option(option, aliases) for (option, aliases) in [
        ('quiet',        ['-q', '--quiet']),
        ('verbose',      ['-v', '--verbose']),
        ('release',      ['-r', '--release']),
        ('developer',    ['-d', '--developer']),
        (action_help,    ['-h', '--help', 'help']),
        (action_version, ['-V', '--version', 'version']),
        (action_new,     ['new']),
        (action_init,    ['init']),
        (action_build,   ['build']),
        (action_run,     ['run']),
        (action_test,    ['test']),
        (action_debug,   ['debug']),
    ]]

def pre_config_actions():
    return [
        action_new,
        action_init,
        action_help,
        action_version,
    ]

def add_option(option, aliases):
    def try_option(arg, options):
        if arg in aliases:
            if is_flag(option):
                add_flag(option, options)
            if is_action(option):
                add_action(option, options)
            return True
    return try_option

def is_flag(option):
    return type(option) == str

def is_action(option):
    return callable(option)

def add_flag(flag, options):
    if options[flag]:
        argument_error(messages.repeated_option.format(flag), flag)
    else:
        options[flag] = True

def add_action(action, options):
    if options['action']:
        argument_error(messages.too_many_arguments, action)
    else:
        options['action'] = action

def try_name(arg, options):
    if not options['action']:
        argument_error(messages.unknown_argument, arg)
    if options['name']:
        argument_error(messages.too_many_arguments, arg)
    options['name'] = arg

def argument_error(message, arg):
    args = ['mekpie'] + debug.args
    panic(f'{message}\n{tab(underline(arg, args))}')