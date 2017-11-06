#!/usr/bin/python3

from model.entity.classes.util import ClassName,BaseClass
from model.entity.weapons import WeaponType

wizard_babs = {
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


class Wizard(BaseClass):

    name = ClassName.wizard

    proficiencies = {
        WeaponType.club,
        WeaponType.dagger,
        WeaponType.heavy_crossbow,
        WeaponType.light_crossbow,
        WeaponType.quarterstaff,
    }

    def __init__(self):
        super().__init__()
        self.bonuses = []
        self.level_up()

