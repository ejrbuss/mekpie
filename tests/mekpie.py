# External Imports
from unittest import TestCase
from os       import curdir, chdir, mkdir
from os.path  import abspath, join, exists
from sys      import path

# Mekpie Imports
from mekpie.core        import mekpie
from mekpie.definitions import Options, MAIN
from mekpie.create      import command_new, command_init
from mekpie.util        import same_dir, srmtree, empty
from mekpie.compiler    import (
    command_clean,
    command_build,
    command_run,
    command_test,
)

root = abspath(curdir)

def reset_dir():
    chdir(root)

def get_options(newdir, command, subargs=[], programargs=[]):
    return Options(
        quiet       = False,
        verbose     = False,
        release     = False,
        developer   = False,
        changedir   = [newdir],
        command     = command,
        debug       = False,
        subargs     = subargs,
        programargs = programargs,
    )

def new_default():
    reset_dir()
    srmtree('./examples/tests/default-project')
    mekpie(get_options(
        './examples/tests',
        command_new,
        ['default-project'],
    ))
    reset_dir()

def cleanup_default():
    reset_dir()
    srmtree('./examples/tests/default-project')

class TestMekpie(TestCase):

    def test_new(self):
        new_default()
        self.assertTrue(same_dir(
            './examples/default-project',
            './examples/tests/default-project',
        ))
        cleanup_default()

    def test_init(self):
        reset_dir()
        srmtree('./examples/tests/default-project')
        mkdir('./examples/tests/default-project')
        mekpie(get_options(
            './examples/tests/default-project',
            command_init,
        ))
        reset_dir()
        self.assertTrue(same_dir(
            './examples/default-project',
            './examples/tests/default-project',
        ))
        srmtree('./examples/tests/default-project')

    def test_test(self):
        new_default()
        with open('./examples/tests/default-project/tests/test1.c', 'w') as resource:
            resource.write(MAIN.replace('Hello, World!', 'test1!') + '\n')
        with open('./examples/tests/default-project/tests/test2.c', 'w') as resource:
            resource.write(MAIN.replace('Hello, World!', 'test2!') + '\n')
        with open('./examples/tests/default-project/tests/test3.c', 'w') as resource:
            resource.write(MAIN.replace('Hello, World!', 'test3!') + '\n')
        results = mekpie(get_options(
            './examples/tests/default-project',
            command_test,
        ))
        out = (
            results.commands[-1].stdout +
            results.commands[-3].stdout +
            results.commands[-5].stdout 
        )
        reset_dir()
        self.assertEqual(out, 'test3!\ntest2!\ntest1!\n')
        results = mekpie(get_options(
            './examples/tests/default-project',
            command_test,
            subargs=['test2', 'test3'],
        ))
        reset_dir()
        out = (
            results.commands[-1].stdout +
            results.commands[-3].stdout
        )
        self.assertEqual(out, 'test3!\ntest2!\n')
        cleanup_default()

    def test_clean(self):
        new_default()
        mekpie(get_options(
            './examples/tests/default-project',
            command_build,
        ))
        reset_dir()
        mekpie(get_options(
            './examples/tests/default-project',
            command_clean,
        ))
        reset_dir()
        self.assertFalse(exists(
            './examples/tests/default-project/target/debug/default-project.o'
        ))
        cleanup_default()

    def test_build(self):
        new_default()
        results = mekpie(get_options(
            './examples/tests/default-project',
            command_build,
        ))
        reset_dir()
        self.assertFalse(empty(results.commands))
        self.assertTrue(
            all(map(lambda c : c.returncode == 0, results.commands))
        )
        self.assertTrue(exists(
            './examples/tests/default-project/target/debug/default-project.o'
        ))
        cleanup_default()

    def test_run(self):
        new_default()
        results = mekpie(get_options(
            './examples/tests/default-project',
            command_run,
        ))
        out = results.commands[-1].stdout
        self.assertEqual(out, 'Hello, World!\n')
        cleanup_default()
