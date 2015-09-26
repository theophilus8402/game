#!/usr/bin/python3.4

import unittest
import model.util

class util(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_bab(self):
        get_bab = model.util.get_bab
        self.assertEqual(get_bab("fighter", 5), [5])
        self.assertEqual(get_bab("monk", 8), [6, 1])
        self.assertEqual(get_bab("paladin", 1), [1])
        self.assertEqual(get_bab("ranger", 2), [2])
        self.assertEqual(get_bab("rogue", 20), [15, 10, 5])
        self.assertEqual(get_bab("sorcerer", 17), [8, 3])
        self.assertEqual(get_bab("wizard", 13), [6, 1])

    def test_get_base_save_bonus(self):
        get_bsb = model.util.get_base_save_bonus
        self.assertEqual(get_bsb("fighter", "fort", 9), 6)
        self.assertEqual(get_bsb("fighter", "will", 14), 4)
        self.assertEqual(get_bsb("monk", "ref", 2), 3)
        self.assertEqual(get_bsb("monk", "will", 11), 7)
        self.assertEqual(get_bsb("paladin", "fort", 3), 3)
        self.assertEqual(get_bsb("ranger", "fort", 4), 4)
        self.assertEqual(get_bsb("rogue", "ref", 20), 12)
        self.assertEqual(get_bsb("sorcerer", "will", 16), 10)
        self.assertEqual(get_bsb("wizard", "fort", 15), 5)

    def test_check_level_up(self):
        check_level_up = model.util.check_level_up
        self.assertTrue(check_level_up(1, 1001))
        self.assertTrue(check_level_up(3, 6100))
        self.assertTrue(check_level_up(5, 17000))
        self.assertTrue(check_level_up(6, 21000))
        self.assertTrue(check_level_up(13, 92225))
        self.assertTrue(check_level_up(16, 137000))
        self.assertTrue(check_level_up(19, 190001))

    def test_max_skill_ranks(self):
        # class max ranks
        class_ranks = model.util.get_class_skill_max_ranks
        self.assertEqual(class_ranks(0), 0)
        self.assertEqual(class_ranks(1), 4)
        self.assertEqual(class_ranks(3), 6)
        self.assertEqual(class_ranks(8), 11)
        self.assertEqual(class_ranks(14), 17)
        self.assertEqual(class_ranks(20), 23)
        self.assertEqual(class_ranks(21), 23)
        # cross-class max ranks
        cross_ranks = model.util.get_cross_class_skill_max_ranks
        self.assertEqual(cross_ranks(0), 0)
        self.assertEqual(cross_ranks(1), 2)
        self.assertEqual(cross_ranks(6), 4.5)
        self.assertEqual(cross_ranks(15), 9)
        self.assertEqual(cross_ranks(16), 9.5)
        self.assertEqual(cross_ranks(20), 11.5)
        self.assertEqual(cross_ranks(21), 11.5)

    def test_check_for_new_attrib(self):
        new_attrib = model.util.check_for_new_attrib
        self.assertTrue(new_attrib(4))
        self.assertTrue(new_attrib(8))
        self.assertTrue(new_attrib(16))
        self.assertTrue(new_attrib(20))
        self.assertFalse(new_attrib(0))
        self.assertFalse(new_attrib(1))
        self.assertFalse(new_attrib(19))

if __name__ == '__main__':
    unittest.main()
