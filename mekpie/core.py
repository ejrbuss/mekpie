# External imports
from os  import curdir, chdir
from sys import argv

# Qualified local imports
import mekpie.debug    as debug
import mekpie.messages as messages

# Local imports
from .util        import rest, panic
from .config      import read_config, config_path
from .arguments   import parse, pre_config_commands

def main(args=rest(argv)):
    debug.args = args
    handle_options(parse(args))

def handle_options(options):
    prepare_for_command(options)
    perform_command(options)

def prepare_for_command(options):
    if options.developer:
        enable_developer_mode()
    if options.changedir:
        chdir(options.name)

def perform_command(options):
    if options.command is None:
        panic(messages.no_command)
    elif options.command in pre_config_commands():
        options.command(options)
    else:
        options.command(options, get_config())

def get_config():
    return read_config(open(config_path(curdir)).read())

def enable_developer_mode():
    debug.enable()