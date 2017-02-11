#!/usr/bin/python3

from model.entity.basic_entity import Entity

# Basic armour:
class Armour(Entity):

    def __init__(self):
        Entity.__init__(self)
        self.type = "armour"      # the different entity classes
        self.base_cost = 0
        self.armour_bonus = 0       # 1,2...
        self.max_dex_bonus = 8      # goes down from there
        self.armour_check_penalty = 0
        self.arcane_spell_fail = 5  # 5%, 10%...
        self.speed = (30, 20)       # different races have different speeds
        self.shield = False         # armour or shield
        self.armour_type = ""       # light, medium, heavy

        self.defence_possibilities = dict()
