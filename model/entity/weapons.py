#!/usr/bin/python3

from model.entity.basic_entity import Entity
from model.entity.living.equip import EqSlots

# Basic weapon:
class Weapon(Entity):

    def __init__(self, cur_hp=0):
        super(Weapon, self).__init__(cur_hp=cur_hp)
        self.type = "weapon"      # the different entity classes
        self.eq_slot = EqSlots.hand
        self.possibilities = {}

        # weapon dmg (2d6)
        self.die_to_roll = 0
        self.dmg_modifier = 0
        self.critical_dmg = 2       # x2
        self.range_increment = 0    # stuff for projectiles
        self.base_cost = 0          # can be modified
        self.weapon_category = ""   # simple, martial, exotic
        self.melee = True           # melee or ranged
        self.weapon_type = ""       # sword, mace
        self.dmg_type = []          # blunt, pierce (can be a combo of em)
        self.size = ""              # tiny, small, medium, large
        self.reach = False          # i.e. glaive can hit 10ft away but not
                                    #   right infront
        self.two_handed = False     # this is only for absolute reqs
                                    #   this doesn't handle large weapon
                                    #   being wielded by a gnome


