# External Imports
from unittest import TestCase
from os       import curdir, chdir, mkdir
from os.path  import abspath, join, exists
from sys      import path

# Mekpie Imports
from mekpie.core        import mekpie
from mekpie.definitions import Options, MAIN
from mekpie.create      import command_new, command_init
from mekpie.util        import same_dir, srmtree, empty, smkdir
from mekpie.compiler    import (
    command_clean,
    command_build,
    command_run,
    command_test,
)

default_project_name = 'default-project'
default_test_dir     = abspath('./examples/tests/')
default_project      = abspath(f'./examples/{default_project_name}/')
default_test_project = abspath(f'./examples/tests/{default_project_name}/')

# sanity
smkdir(default_test_dir)

def clean_test_dir():
    srmtree(default_test_project)

def get_options(command, subargs=[], cdir=default_test_project):
    return Options(
        quiet       = False,
        verbose     = False,
        release     = False,
        developer   = False,
        changedir   = [cdir],
        command     = command,
        debug       = True,
        subargs     = subargs,
        programargs = [],
    )

def effective_program(path):
    path = path.replace('\\', '\\\\')
    return f'''
#include <stdio.h>
#include <stdlib.h>

int main() {{
    FILE *fp;
    fp = fopen("{path}", "w");
    fclose(fp);
    return EXIT_SUCCESS;
}}

'''

class TestProject():

    def __enter__(self):
        clean_test_dir()
        mekpie(get_options(
            command_new,
            [default_project_name],
            default_test_dir,
        ))

    def __exit__(self, type, value, traceback):
        clean_test_dir()


class TestMekpie(TestCase):

    def test_new(self):
        with TestProject():
            self.assertTrue(same_dir(
                default_project,
                default_test_project,
            ))

    def test_init(self):
        clean_test_dir()
        smkdir(default_test_project)
        mekpie(get_options(command_init))
        self.assertTrue(same_dir(
            default_project,
            default_test_project,
        ))
        clean_test_dir()

    def test_test(self):
        with TestProject():
            test1 = default_test_project + '/test1.txt'
            test2 = default_test_project + '/test2.txt'
            test3 = default_test_project + '/test3.txt'
            with open(default_test_project + '/tests/test1.c', 'w') as rsc:
                rsc.write(effective_program(test1))
            with open(default_test_project + '/tests/test2.c', 'w') as rsc:
                rsc.write(effective_program(test2))
            with open(default_test_project + '/tests/test3.c', 'w') as rsc:
                rsc.write(effective_program(test3))
            mekpie(get_options(command_test, ['test2', 'test3']))
            self.assertFalse(exists(test1))
            self.assertTrue(exists(test2))
            self.assertTrue(exists(test3))
            mekpie(get_options(command_test))
            self.assertTrue(exists(test1))
            self.assertTrue(exists(test2))
            self.assertTrue(exists(test3))

    def test_clean(self):
        with TestProject():
            mekpie(get_options(command_build))
            mekpie(get_options(command_clean))
            self.assertFalse(exists(
                default_test_project + '/target/debug/default-project.o'
            ))

    def test_build(self):
        with TestProject():
            results = mekpie(get_options(command_build))
            self.assertFalse(empty(results.commands))
            self.assertTrue(exists(
                default_test_project + '/target/debug/default-project.o'
            ))

    def test_run(self):
        with TestProject():
            build = abspath(default_test_project + '/build.txt')
            with open(default_test_project + '/src/default-project.c', 'w') as rsc:
                rsc.write(effective_program(build))
            mekpie(get_options(command_run))
            self.assertTrue(exists(build))