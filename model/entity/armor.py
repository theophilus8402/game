#!/usr/bin/python3

from enum import Enum,unique

from model.entity.basic_entity import Entity

ArmorType = Enum("ArmorType", [
    "spiked_armor",
    "light_armor",
    "medium_armor",
    "heavy_armor",
    ])

# Basic armor:
class Armor(Entity):

    def __init__(self):
        Entity.__init__(self)
        self.type = "armor"      # the different entity classes
        self.base_cost = 0
        self.armor_bonus = 0       # 1,2...
        self.max_dex_bonus = 8      # goes down from there
        self.armor_check_penalty = 0
        self.arcane_spell_fail = 5  # 5%, 10%...
        self.speed = (30, 20)       # different races have different speeds
        self.shield = False         # armour or shield
        self.armor_type = ""       # light, medium, heavy

        self.possibilities = dict()
