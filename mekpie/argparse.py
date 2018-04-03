import collections

Parsedargs = collections.namedtuple('Parsedargs', ['command', 'args', 'options'])

def parse(args):
    """
    Should return a Parsedargs instance
    {
        command : 'help|version|new|init|test|build|clean|run|error'
        name    : string
        quiet   : bool
        release : bool
    }
    """
    pass