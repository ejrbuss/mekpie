# External imports
from os  import curdir, chdir
from sys import argv

# Qualified local imports
import mekpie.debug    as debug
import mekpie.messages as messages

# Local imports
from .util      import cdr, panic, file_as_str
from .config    import read_config, config_path
from .arguments import parse, pre_config_commands

def main(args=cdr(argv)):
    debug.args = args
    handle_options(parse(args))

def handle_options(options):
    prepare_for_command(options)
    perform_command(options)

def prepare_for_command(options):
    if options.developer:
        debug.enable()
    if options.changedir:
        chdir(options.name)

def perform_command(options):
    command = options.command
    if command is None:
        panic(messages.no_command)
    elif command in pre_config_commands():
        command(options)
    else:
        command(options, get_config())

def get_config():
    return read_config(file_as_str(config_path(curdir)))