#!/usr/bin/python3

from model.bonuses import BonusReason
from model.entity.classes.util import ClassName, class_name_map
from model.entity.living.attack_bonus import AttackBonus
from model.entity.weapons import WeaponType

from collections import defaultdict


wizard_bab_map = {
    1 : [0],
    2 : [1],
    3 : [1],
    4 : [2],
    5 : [2],
    6 : [3],
    7 : [3],
    8 : [8, 3],
    9 : [9, 4],
    10 : [10, 5],
    11 : [11, 6, 1],
    12 : [12, 7, 2],
    13 : [13, 8, 3],
    14 : [14, 9, 4],
    15 : [15, 10, 5],
    16 : [16, 11, 6, 1],
    17 : [17, 12, 7, 2],
    18 : [18, 13, 8, 3],
    19 : [19, 14, 9, 4],
    20 : [20, 15, 10, 5],
}


class Wizard():

    name = ClassName.wizard

    proficiencies = {
        WeaponType.club,
        WeaponType.dagger,
        WeaponType.heavy_crossbow,
        WeaponType.light_crossbow,
        WeaponType.quarterstaff,
    }

    def __init__(self):
        self.bonuses = []
        self.level = 1
        self.class_bab = AttackBonus(wizard_bab_map[self.level], BonusReason.entity_class)

    def __repr__(self):
        return "<{} : {}>".format(self.name.name, self.level)

    def level_up(self):
        self.level += 1
        self.class_bab.amount = wizard_bab_map[self.level]


class_name_map[ClassName.wizard] = Wizard
