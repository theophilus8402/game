#!/usr/bin/python3.4

import unittest
import model.util

class util(unittest.TestCase):

    def setUp(self):
        pass

    def test_roll(self):
        roll = model.util.roll
        self.assertEqual(roll(1, 1), 1)
        self.assertEqual(roll(1, 1, 1), 2)
        self.assertNotEqual(roll(1, 1, 2), 2)

        for i in range(100):
            self.assertTrue(3 <= roll(3, 20) <= 60)
            self.assertTrue(-1 <= roll(1, 10, -2) <= 8)
            self.assertTrue(5 <= roll(2, 15, 3) <= 33)


if __name__ == '__main__':
    unittest.main()
