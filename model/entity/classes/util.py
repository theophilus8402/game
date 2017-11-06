
from enum import unique, Enum


ClassName = Enum("ClassName", [
    "barbarian",
    "bard",
    "cleric",
    "druid",
    "fighter",
    "monk",
    "paladin",
    "ranger",
    "rogue",
    "sorcerer",
    "wizard",
])

class_name_map = {}

class_babs = {}

def get_bab(class_name, class_level):
    return class_babs[class_name][class_level]


class BaseClass():

    def __init__(self):
        self.level = 0
        self.class_bab = []
        self.level_up()

    def __repr__(self):
        return "<{} : {}>".format(self.name.name, self.level)

    def level_up(self):
        self.level += 1
        # do other things like set class_attack_bonus, feats, abilities
        self.class_bab = get_bab(self.name, self.level)

