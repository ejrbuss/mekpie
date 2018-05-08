# External imports
from sys     import stderr
from re      import sub
from os.path import isfile, isdir

# Qualified local imports
import mekpie.debug    as debug
import mekpie.messages as messages

def panic(message):
    errprint(f'\n{message.strip()}\n')
    raise Exception('Debug') if debug.debug else exit(1)

def errprint(string):
    stderr.write(string)

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
    panic(messages.file_not_found.format(path))

def check_is_dir(path):
    if isdir(path):
        return path
    panic(messages.directory_not_found.format(path))

def type_name(x):
    return type(x).__name__
