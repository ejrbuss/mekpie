# External Imports
from subprocess import run, PIPE
from select     import select
from sys        import stdout, stderr

# Qualified local imports
import mekpie.messages as messages

# Internal Imports
from .definitions import MekpieResult, Command
from .util        import panic, log, car, last

commands = []

def lrun(args, quiet=False, error=True):
    try:
        commands.append(create_command(args, run_args(args, quiet)))
        return last(commands)
    except OSError:
        if error:
            panic(messages.failed_program_call.format(serialize_command(args)))

def run_args(args, quiet):
    if quiet:
        return run(args, stdout=PIPE, stderr=PIPE)
    else:
        return run(args)


def create_command(args, proc):
    return Command(
        args       = args,
        sargs      = serialize_command(args),
        stdout     = (proc.stdout or b'').decode('utf-8'),
        stderr     = (proc.stderr or b'').decode('utf-8'),
        returncode = proc.returncode,
    )

def serialize_command(args):
    return '$ ' + ' '.join(args)
