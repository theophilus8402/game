
from model.bonuses import BonusReason
from model.entity.classes.util import ClassName,class_name_map
from model.entity.living.attack_bonus import AttackBonus
from model.entity.weapons import simple_weapon_group,martial_weapon_group
from model.entity.armor import ArmorType


barbarian_bab_map = {
    1 : [1],
    2 : [2],
    3 : [3],
    4 : [4],
    5 : [5],
    6 : [6, 1],
    7 : [7, 2],
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

class Barbarian():

    name = ClassName.barbarian

    def __init__(self):
        self.bonuses = []
        self.level = 1
        self.class_bab = AttackBonus(barbarian_bab_map[self.level], BonusReason.entity_class)
        self.proficiencies = {
            *simple_weapon_group,
            *martial_weapon_group,
            ArmorType.light_armor,
            ArmorType.medium_armor,
            ArmorType.shield
        }

    def __repr__(self):
        return "<{} : {}>".format(self.name.name, self.level)

    def level_up(self):
        self.level += 1
        # do other things like set class_attack_bonus, feats, abilities
        self.class_bab.amount = barbarian_bab_map[self.level]


class_name_map[ClassName.barbarian] = Barbarian
