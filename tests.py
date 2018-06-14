# External Imports
from subprocess import run
from sys        import stderr
from os         import listdir
from os.path    import join

# Python3.8 command line name
python = 'python3'

# Run a test file
def test(path):
    stderr.write(f' -- Running {path}...\n')
    stderr.flush()
    run(f'{python} -m unittest {path}'.split())

# Gather test paths
paths = [join('tests/', path)
    for path 
    in listdir('./tests') 
    if path.endswith('.py') and not path.startswith('__')]

# Run tests
[test(path) for path in paths]