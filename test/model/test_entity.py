#!/usr/bin/python3.4

import unittest

from model.entity.entity import change_hp
from model.entity.status_effects import *
import play

class util(unittest.TestCase):

    def setUp(self):
        self.bob = play.make_bob()
        self.sword = play.make_sword()
        self.shield = play.make_shield()

    def test_can_move(self):
        # NOTE: also testing add_status()
        self.assertEqual(self.bob.can_move(), (True, None))

        add_status_effect(self.bob, Afflictions.stupid)
        self.assertEqual(self.bob.status_effects, {Afflictions.stupid})
        self.assertEqual(self.bob.can_move(), (True, None))

        add_status_effect(self.bob, Afflictions.paralysis)
        self.assertEqual(self.bob.can_move(), (False, Afflictions.paralysis))

        remove_status_effect(self.bob, Afflictions.stupid)
        self.assertEqual(self.bob.status_effects, {Afflictions.paralysis})
        remove_status_effect(self.bob, Afflictions.paralysis)
        self.assertEqual(self.bob.status_effects, set())
        self.assertEqual(self.bob.can_move(), (True, None))

        add_status_effect(self.bob, Afflictions.lost_balance)
        self.assertEqual(self.bob.can_move(), (False, Afflictions.lost_balance))

    def test_wield_unwield(self):
        """
        self.bob.wield("right", self.sword)
        self.assertEqual(self.bob.eq["right_hand"], self.sword)
        # sword gives +1 attack_bonus
        misc_attack_bonus, misc_attack_list = self.bob.attack_bonus["misc"]
        self.assertEqual(misc_attack_bonus, 1)
        self.assertEqual(misc_attack_list, [self.sword])

        # errors
        status = self.bob.wield("right", self.sword)
        self.assertEqual(status, 4) # already wielding something in that hand

        # wield shield in left +1 ac
        self.assertEqual(self.bob.wield("left", self.shield), 0)
        self.assertEqual(self.bob.eq["left_hand"], self.shield)
        self.assertEqual(self.bob.ac["shield"], 1)

        # unwield sword
        self.assertEqual(self.bob.unwield("right"), 0)
        self.assertEqual(self.bob.eq["right_hand"], None)
        misc_attack_bonus, misc_attack_list = self.bob.attack_bonus["misc"]
        self.assertEqual(misc_attack_bonus, 0)
        self.assertEqual(misc_attack_list, [])

        # error unwield (nothing in the hand)
        self.assertEqual(self.bob.unwield("right"), 5)

        # unwield shield
        self.assertEqual(self.bob.unwield("left"), 0)
        self.assertEqual(self.bob.eq["left_hand"], None)
        self.assertEqual(self.bob.ac["shield"], 0)
        """
        pass

    def test_change_hp(self):
        self.bob.cur_hp = 10
        change_hp(self.bob, 10)
        self.assertEqual(self.bob.cur_hp, 20)

        change_hp(self.bob, -30)
        self.assertEqual(self.bob.cur_hp, -10)

    def test_die(self):
        #TODO: there might be more to do in the future
        # But for now, all it's supposed to do is add "dead" to the
        #   status_msgs
        self.assertFalse(Afflictions.dead in self.bob.status_effects)
        self.bob.die()
        self.assertTrue(Afflictions.dead in self.bob.status_effects)

    def test_calculate_ac(self):
        """
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
        """
        pass
        

    def test_add_remove_armour_bonus(self):
        # errors
        """
        self.assertEqual(self.bob.add_armour_bonus("total", 2), 1)
        self.assertEqual(self.bob.add_armour_bonus("misc", 2), 2)

        self.bob.add_armour_bonus("armour", 2)
        self.assertEqual(self.bob.ac["total"], 15)

        self.bob.add_armour_bonus("shield", 1)
        self.assertEqual(self.bob.ac["total"], 16)

        #TODO: test "misc" items, but I don't have any for now

        # ALSO testing remove_armour_bonus
        # errors
        self.assertEqual(self.bob.remove_armour_bonus("total", 2), 1)
        self.assertEqual(self.bob.remove_armour_bonus("misc", 2), 2)

        self.bob.remove_armour_bonus("armour", 2)
        self.assertEqual(self.bob.ac["total"], 14)

        self.bob.remove_armour_bonus("shield", 1)
        self.assertEqual(self.bob.ac["total"], 13)
        """
        pass


if __name__ == '__main__':
    unittest.main()

