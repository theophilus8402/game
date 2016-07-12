
import unittest

from model.entity.util import *
import play

class SetAbility(unittest.TestCase):

    def setUp(self):
        self.bob = play.make_bob()
        self.bob.level = 1
        self.bob.abilities = {}
        set_ability(self.bob, Ability.strength, 14)
        set_ability(self.bob, Ability.dexterity, 15)
        set_ability(self.bob, Ability.constitution, 13)
        set_ability(self.bob, Ability.intelligence, 11)
        set_ability(self.bob, Ability.wisdom, 11)
        set_ability(self.bob, Ability.charisma, 10)

        self.sword = play.make_sword()
        self.bow = play.make_bow()

    def test_set_ability(self):
        self.assertEqual(self.bob.abilities[Ability.strength], (14, 2))
        self.assertEqual(self.bob.abilities[Ability.dexterity], (15, 2))
        self.assertEqual(self.bob.abilities[Ability.constitution], (13, 1))
        self.assertEqual(self.bob.abilities[Ability.intelligence], (11, 0))
        self.assertEqual(self.bob.abilities[Ability.wisdom], (11, 0))
        self.assertEqual(self.bob.abilities[Ability.charisma], (10, 0))

        set_ability(self.bob, Ability.intelligence, 20)
        set_ability(self.bob, Ability.wisdom, 8)
        set_ability(self.bob, Ability.charisma, 7)
        self.assertEqual(self.bob.abilities[Ability.intelligence], (20, 5))
        self.assertEqual(self.bob.abilities[Ability.wisdom], (8, -1))
        self.assertEqual(self.bob.abilities[Ability.charisma], (7, -2))

    def test_get_modifier(self):
        self.assertEqual(get_ability_modifier(self.bob, Ability.strength), 2)
        self.assertEqual(get_ability_modifier(self.bob, Ability.dexterity), 2)
        self.assertEqual(get_ability_modifier(self.bob, Ability.constitution), 1)
        self.assertEqual(get_ability_modifier(self.bob, Ability.intelligence), 0)
        self.assertEqual(get_ability_modifier(self.bob, Ability.wisdom), 0)
        self.assertEqual(get_ability_modifier(self.bob, Ability.charisma), 0)

        set_ability(self.bob, Ability.wisdom, 8)
        set_ability(self.bob, Ability.charisma, 7)
        self.assertEqual(get_ability_modifier(self.bob, Ability.wisdom), -1)
        self.assertEqual(get_ability_modifier(self.bob, Ability.charisma), -2)

    def test_get_proficiency_modifier(self):
        self.assertEqual(get_proficiency_modifier(self.bob,
            Proficiency.simple_weapons), 2)

    def test_get_attack_bonus(self):
        # short sword is finesse (so dex stuff)
        # bob: dex = 15, fighter, lvl 1
        # att_bonus = dex_mod + prof_bonus = 2 + 2 = 4
        self.assertEqual(get_attack_bonus(self.bob, self.sword, melee=True), 4)

        set_ability(self.bob, Ability.dexterity, 18)
        # bob: fighter, lvl 1
        # att_bonus = dex_mod + prof_bonus = 4 + 2 = 6
        self.assertEqual(get_attack_bonus(self.bob, self.bow, melee=False), 6)

        self.bob.level = 7
        # bob: dex = 18, fighter, lvl 7
        # att_bonus = dex_mod + prof_bonus = 4 + 3 = 7
        self.assertEqual(get_attack_bonus(self.bob, self.sword, melee=True), 7)

        self.bob.level = 18
        # bob: fighter, lvl 18
        # att_bonus = dex_mod + prof_bonus = 4 + 6 = 10
        self.assertEqual(get_attack_bonus(self.bob, self.bow, melee=False), 10)

        self.sword.properties = []
        # bob: str = 14, fighter, lvl 7
        # att_bonus = str_mod + prof_bonus = 2 + 6 = 8
        self.assertEqual(get_attack_bonus(self.bob, self.sword, melee=True), 8)

