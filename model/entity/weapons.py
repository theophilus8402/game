#!/usr/bin/python3

from enum import Enum,unique
from random import choice

from model.entity.basic_entity import Entity
from model.entity.living.equip import EqSlots

WeaponType = Enum("WeaponName", [
    "gauntlet",
    "unarmed_strike",
    "dagger",
    "punching_dagger",
    "spiked_gauntlet",
    "light_mace",
    "sickle",
    "club",
    "heavy_mace",
    "morningstar",
    "shortspear",
    "longspear",
    "quarterstaff",
    "spear",
    "blowgun",
    "heavy_crossbow",
    "light_crossbow",
    "dart",
    "javelin",
    "sling",
    "throwing_axe",
    "light_hammer",
    "handaxe",
    "kukri",
    "light_pick",
    "sap",
    "spiked_armor",
    "starknife",
    "short_sword",
    "battleaxe",
    "flail",
    "longsword",
    "heavy_pick",
    "rapier",
    "scimitar",
    "trident",
    "warhammer",
    "falchion",
    "glaive",
    "greataxe",
    "greatclub",
    "heavy_flail",
    "greatsword",
    "guisarme",
    "halberd",
    "lance",
    "ranseur",
    "scythe",
    "longbow",
    "composite_longbow",
    "shortbow",
    "composite_shortbow",
    "kama",
    "nunchaku",
    "sai",
    "siangham",
    "bastard_sword",
    "dwarven_waraxe",
    "whip",
    "orc_double_axe",
    "spiked_chain",
    "elven_curve_blade",
    "dire_flail",
    "gnome_hooked_hammer",
    "two_bladed_sword",
    "dwarven_urgrosh",
    "bolas",
    "hand_crossbow",
    "repeating_heavy_crossbow",
    "repeating_light_crossbow",
    "net",
    "shuriken",
    "halfling_sling_staff",
     ])

DmgType = Enum("DmgType", [
    "bludgeoning",
    "piercing",
    "slashing",
    ])

WeaponSpecial = Enum("WeaponSpecial", [
    "brace",
    "disarm",
    "double",
    "monk",
    "nonlethal",
    "reach",
    "trip",
    ])

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

    def get_damage(self):
        dmg_results = {}
        for dmg_type, (base_amt, dmg_range) in self.damage.items():
            result = choice(range(base_amt-dmg_range, base_amt+dmg_range+1))
            dmg_results[dmg_type] = result
        return dmg_results
