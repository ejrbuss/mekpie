# External imports
from sys     import stderr
from re      import sub
from os.path import isfile, isdir

# Qualified local imports
import mekpie.debug as debug

def panic(message):
    stderr.write(f'\n{message.strip()}\n')
    if debug.debug:
        raise Exception('Debug')
    else:
        exit(1)

def empty(collection):
    return len(collection) == 0

def rest(collection):
    return collection[1:]

def tab(string, spaces=4):
    return sub(r'^|\n', '\n' + (spaces * ' '), string)

def underline(element, collection):
    top = ' '.join(collection)
    bottom = ' '.join(underlined_collection(element, collection))
    return f'{top}\n{bottom}'

def underlined_collection(underlined_element, collection):
    def underline_or_hide(element):
        return sub(
            r'.',
            '^' if element == underlined_element else ' ',
            str(element)
        )
    return map(underline_or_hide, collection)

def check_is_file(path):
    if isfile(path):
        return path
    panic(f'File not found: Could not find "{path}"!')

def check_is_dir(path):
    if isdir(path):
        return path
    panic(f'Directory not found: Could not find "{path}"!')

def type_name(x):
    return type(x).__name__
