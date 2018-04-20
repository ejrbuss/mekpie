from os.path import join, curdir

def get_project_path(name):
    return join(curdir, name)

def get_mekpy_path(name):
    return join(get_project_path(name), 'mek.py')

def get_src_path(name):
    return join(get_project_path(name), 'src')

def get_main_path(name, main):
    return join(get_src_path(name), main)

def get_test_path(name):
    return join(get_project_path(name), 'tests')

def get_includes_path(name):
    return join(get_project_path(name), 'includes')

def get_target_path(name):
    return join(get_project_path(name), 'target')

def get_target_debug_path(name):
    return join(get_target_path(name), 'debug')

def get_target_release_path(name):
    return join(get_target_path(name), 'release')

def get_target_tests_path(name):
    return join(get_target_path(name), 'tests')