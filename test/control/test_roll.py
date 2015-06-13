#!/usr/bin/python3.4

import unittest
import control.roll

#roll(num_die, sides, modifier)
class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_basic(self):
        result = control.roll.roll(1, 1, 2)
        self.assertNotEqual(result, 2)

if __name__ == '__main__':
    unittest.main()
