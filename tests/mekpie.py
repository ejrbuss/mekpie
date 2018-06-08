# External Imports
from unittest import TestCase
from os       import curdir, chdir, mkdir
from os.path  import abspath, join, exists
from sys      import path

# Mekpie Imports
from mekpie.core        import mekpie
from mekpie.definitions import Options
from mekpie.create      import command_new, command_init
from mekpie.util        import same_dir, srmtree

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

class TestMekpie(TestCase):
    
    def test_new(self):
        reset_dir()
        srmtree('./examples/tests/default-project')
        mekpie(get_options(
            './examples/tests',
            command_new,
            ['default-project'],
        ))
        reset_dir()
        self.assertTrue(same_dir(
            './examples/default-project',
            './examples/tests/default-project',
        ))
        srmtree('./examples/tests/default-project')

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