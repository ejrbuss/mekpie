# External Imports
from subprocess import Popen, PIPE
from select     import select
from sys        import stdout, stderr

# Qualified local imports
import mekpie.messages as messages

# Internal Imports
from .definitions import MekpieResult, Command
from .util        import panic, log, car

commands = []

def lrun(args, quiet=False, error=True):
    command = Command(**default_command(args))
    try:
        command = capture_command(args, quiet)
    except OSError:
        if error:
            panic(messages.failed_program_call.format(serialize_command(args)))
    commands.append(command)
    return command

def capture_command(args, quiet=False):
    with create_process(args) as process:
        command = default_command(args)
        command['returncode'] = handle_streams(
            process, 
            buffer(command, quiet),
        )
        return Command(**command)

def buffer(command, quiet):
    def handler(stream, iostream, name):
        content = stream.readline().decode('utf-8')
        command[name] += content
        if not quiet:
            iostream.write(content)
    return handler

def create_process(args):
    log('Running ' + serialize_command(args))
    return Popen(args, stdout=PIPE, stderr=PIPE)

def default_command(args):
    return {
        'args'       : args,
        'sargs'      : serialize_command(args),
        'stdout'     : '',
        'stderr'     : '',
        'returncode' : 0,
    }

def handle_streams(process, callback):
    return_code = None
    streams     = [
        (process.stdout, stdout, 'stdout'),
        (process.stderr, stderr, 'stderr'),
    ]
    while return_code is None:
        fds = get_file_descriptors(streams)
        for fd in car(select(fds, [], [])):
            idx = fds.index(fd)
            callback(*(streams[idx]))
        return_code = process.poll()
    return return_code

def get_file_descriptors(streams):
    return list(map(lambda s : car(s).fileno(), streams))

def serialize_command(args):
    return '$ ' + ' '.join(args)

def decode_proc(proc):
    proc.stdout = proc.stdout.decode('utf-8')
    proc.stderr = proc.stderr.decode('utf-8')
    return proc