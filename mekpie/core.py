# External imports
from os  import curdir
from sys import argv

# Qualified local imports
import mekpie.debug    as debug
import mekpie.messages as messages

# Local imports
from .util        import rest, panic
from .config      import read_config, config_path
from .arguments   import parse, pre_config_actions

def main(args=rest(argv)):
    debug.args = args
    handle_options(parse(args))

def handle_options(options):
    prepare_for_action(options)
    perform_action(options)

def prepare_for_action(options):
    if options.developer:
        enable_developer_mode()

def perform_action(options):
    if options.action is None:
        panic(messages.no_action)
    elif options.action in pre_config_actions():
        options.action(options)
    else:
        options.action(options, get_config())

def get_config():
    return read_config(open(config_path(curdir)).read())

def enable_developer_mode():
    debug.enable()