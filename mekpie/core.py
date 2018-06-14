# External imports
from os  import curdir, chdir
from sys import argv

# Qualified local imports
import mekpie.debug    as debug
import mekpie.messages as messages

# Local imports
from .util        import log, car, cdr, panic, file_as_str
from .config      import read_config, config_path
from .arguments   import parse, pre_config_commands
from .definitions import Options

def mekpie(options):
    if type(options) != Options:
        panic(messages.api_no_options)
    prepare_for_command(options)
    perform_command(options)

def main(args=cdr(argv)):
    debug.args = args
    mekpie(parse(args))

def prepare_for_command(options):
    if options.developer:
        debug.enable()
    if options.changedir:
        chdir(car(options.changedir))

def perform_command(options):
    command = options.command
    if command is None:
        panic(messages.no_command)
    elif command in pre_config_commands():
        command(log(options))
    else:
        command(log(options), log(get_config()))

def get_config():
    return read_config(file_as_str(config_path(curdir)))