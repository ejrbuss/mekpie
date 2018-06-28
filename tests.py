# External Imports
from subprocess import run
from sys        import stderr
from os         import listdir, mkdir
from os.path    import join, exists

# Python3.8 command line name
python = 'python'
# Even developers need reminders
notice = f'''
[Notice]

 If tests are failing remember:
  - point `python` in test.py to python3 (currently `{python}`)
  - rebuild the default-project

[Tests]
'''

# Print the notice
print(notice)

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