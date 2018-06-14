![](/resources/logo.svg)
# A `C` Build System Written in Python

## Creating a Project

```bash
$ mekpie new "project"
```

## Project Structure

```python
project/          # the project directory
    target/       # managed automatically by mekpie
        debug/    # stores the debug binary
        release/  # stores the release binary
        tests/    # stores the test binaries
    includes/     # stores all project .h files
    src/          # stores all project .c files
        project.c # should contain `main`
    tests/        # should contain all test files
    mek.py        # used to configure mekpie
```

## The mek.py File

A typical `mek.py` file:
```python
name = 'project'
libs = [
    'm',
    'pthread',
]
```

All options available for `mek.py`
```python
# the name of the project
name = 'project'
# the c compiler to use
cc = 'gcc'
# the .c file containing `main`
main = './src/project.c'
# libraries to be linked
libs = [...]
```

## Commands

```
Usage:
    mekpie <command> [<args>...]
    mekpie [options]

Options:
    -h, --help    Display this message
    -V, --version Print version info and exit
    -v, --verbose Use verbose output
    -q, --quiet   No output to stdout
    -r, --release Run the command for release

Commands:
    new <name>  Create a new mekpie project
    init <name> Create a project in an existing directory
    test <name> Build and execute tests or test
    build       Compile the current project
    clean       Remove the target directory
    run         Build and execute main
```