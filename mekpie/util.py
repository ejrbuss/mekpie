# External imports
from sys     import stderr
from re      import sub
from os      import walk
from os.path import isfile, isdir, join, basename, splitext

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

def flatten(collection):
    return sum(collection, [])

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

def list_files(path, with_filter=None, with_ext=None, recursive=False):
    if with_filter is None:
        with_filter = lambda : True
    if with_ext is not None:
        with_filter = lambda filename : filename.endswith(with_ext)
    return list(filter(with_filter, list_all_files(path)))

def list_all_files(path):
    return flatten([[join(pre, post)
            for post 
            in posts] 
        for (pre, _, posts) 
        in walk(path)
    ])

def filename(path):
    return splitext(basename(path))[0]

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
