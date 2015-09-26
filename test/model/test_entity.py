#!/usr/bin/python3.4

import unittest
import model.entity
import play

class util(unittest.TestCase):

    def setUp(self):
        self.bob = play.make_bob()
        self.sword = play.make_sword()

    def test_set_attrib(self):
        self.bob.set_attrib("str", 20)
        self.assertEqual(self.bob.attrib["str"], (20, 5))

        self.bob.set_attrib("dex", 15)
        self.assertEqual(self.bob.attrib["dex"], (15, 2))

        self.bob.set_attrib("con", 11)
        self.assertEqual(self.bob.attrib["con"], (11, 0))

        self.bob.set_attrib("int", 1)
        self.assertEqual(self.bob.attrib["int"], (1, -5))

        self.bob.set_attrib("wis", 8)
        self.assertEqual(self.bob.attrib["wis"], (8, -1))

        self.bob.set_attrib("cha", 10)
        self.assertEqual(self.bob.attrib["cha"], (10, 0))

    def test_can_move(self):
        # NOTE: also testing add_status()
        self.bob.status_msgs = []
        self.assertEqual(self.bob.can_move(), (True, None))

        self.bob.add_status("stupid")
        self.assertEqual(self.bob.status_msgs, ["stupid"])
        self.assertEqual(self.bob.can_move(), (True, None))

        self.bob.add_status("paralyzed")
        self.assertEqual(self.bob.can_move(), (False, "paralyzed"))

        self.bob.remove_status("stupid")
        self.assertEqual(self.bob.status_msgs, ["paralyzed"])
        self.bob.remove_status("paralyzed")
        self.assertEqual(self.bob.status_msgs, [])
        self.assertEqual(self.bob.can_move(), (True, None))

        self.bob.add_status("lost balance")
        self.assertEqual(self.bob.can_move(), (False, "lost balance"))

    def test_attack_roll(self):
        #TODO
        pass

    def test_wield(self):
        #TODO
        pass

    def test_unwield(self):
        #TODO
        pass

    def test_change_hp(self):
        #TODO
        pass

    def test_die(self):
        #TODO
        pass

    def test_calculate_ac(self):
        self.bob.ac["armour"] = 0
        self.bob.ac["shield"] = 0
        self.bob.ac["misc"] = (0, None)
        # dex = 15, +2
        # size = "small", +1
        self.bob.calculate_ac()
        self.assertEqual(self.bob.ac["total"], 13)

        self.bob.ac["armour"] = 3
        self.bob.calculate_ac()
        self.assertEqual(self.bob.ac["total"], 16)

        self.bob.ac["shield"] = 1
        self.bob.calculate_ac()
        self.assertEqual(self.bob.ac["total"], 17)

        self.bob.ac["misc"] = (4, ["spiffy"])
        self.bob.calculate_ac()
        self.assertEqual(self.bob.ac["total"], 21)

    def test_add_armour_bonus(self):
        # errors
        self.assertEqual(self.bob.add_armour_bonus("total", 2), 1)
        self.assertEqual(self.bob.add_armour_bonus("misc", 2), 2)

        self.bob.add_armour_bonus("armour", 2)
        self.assertEqual(self.bob.ac["total"], 15)
        #TODO


if __name__ == '__main__':
    unittest.main()
