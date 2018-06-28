# External Imports
from unittest   import TestCase
import sys

# Mekpie Imports
from mekpie.util import (
    empty,
    car,
    last,
    cdr,
    cons,
    shift,
    flatten,
    tab,
    underline,
)

class TestUtil(TestCase):

    def test_empty(self):
        self.assertTrue(empty([]))
        self.assertTrue(empty({}))
        self.assertTrue(empty(''))
        self.assertFalse(empty([1, 2, 3]))
        self.assertFalse(empty({ 'x' : 'y' }))
        self.assertFalse(empty('test'))

    def test_car(self):
        self.assertIsNone(car([]))
        self.assertEqual(car([1, 2, 3]), 1)

    def test_last(self):
        self.assertIsNone(last([]))
        self.assertEqual(last([1, 2, 3]), 3)

    def test_cdr(self):
        self.assertIsNone(cdr([]))
        self.assertEqual(cdr([1, 2, 3]), [2, 3])

    def test_cons(self):
        self.assertEqual(cons(4, [1, 2, 3]), [4, 1, 2, 3])

    def test_shift(self):
        collection = [1, 2, 3, 4, 5]
        shift(collection)
        self.assertEqual(collection, [2, 3, 4, 5])
        shift(collection, 3)
        self.assertEqual(collection, [5])

    def test_flatten(self):
        self.assertEqual(flatten([[1, 2], [3, 4]]), [1, 2, 3, 4])

    def test_tab(self):
        self.assertEqual(
            tab('hello\nworld'),
            '\n    hello\n    world',
        )
        self.assertEqual(
            tab('a  \n b', 2),
            '\n  a  \n   b',
        )

    def test_underline(self):
        self.assertEqual(
            underline('3', ['1', '2', '3', '4']),
            '1 2 3 4\n    ^  ',
        )
