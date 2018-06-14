# External Imports
from unittest import TestCase
from os       import curdir, chdir, mkdir
from os.path  import abspath, join, exists
from sys      import path

# Mekpie Imports
from mekpie.core        import mekpie
from mekpie.definitions import Options
from mekpie.create      import command_new, command_init
from mekpie.util        import same_dir, srmtree, empty
from mekpie.compiler    import command_build, command_run

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

    def test_build(self):
        new_default()
        results = mekpie(get_options(
            './examples/tests/default-project',
            command_build,
        ))
        self.assertFalse(empty(results.commands))
        self.assertTrue(all(map(lambda c : c.returncode == 0, results.commands)))
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

    def test_test(self):
        new_default()
        # insert test files
        # run all testz
        # run individual tests
        cleanup_default()
