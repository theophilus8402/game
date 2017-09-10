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

dmg_type_str_map = {
    DmgType.bludgeoning : "B",
    DmgType.piercing : "P",
    DmgType.slashing : "S",
    }

WeaponSpecial = Enum("WeaponSpecial", [
    "brace",
    "disarm",
    "double",
    "monk",
    "nonlethal",
    "reach",
    "trip",
    ])

WeaponCategory = Enum("WeaponCategory", [
    "light_melee",
    "one_handed_melee",
    "two_handed_melee",
    "ranged",
    ])

# Basic weapon:
class Weapon(Entity):

    def __init__(self, weapon_type=WeaponType.gauntlet, category=WeaponCategory.light_melee, cost=100, dmg="0d0", crit="20x0", weapon_range=0, weight=0, dmg_types=[DmgType.bludgeoning], specials=[], cur_hp=0):
        super(Weapon, self).__init__(cur_hp=cur_hp)
        self.weapon_type = weapon_type
        self.eq_slot = EqSlots.hand

        self.cost = cost

        # weapon dmg (2d6)
        self.num_dice,self.num_side = map(int, dmg.split("d"))
        self.dmg_types = dmg_types

        # crit info, crit_range is lowest number
        self.crit_range,self.crit_dmg = map(int, crit.split("x"))

        self.weapon_range = weapon_range
        self.weight = weight
        self.specials = specials

    def __repr__(self):
        dmg_types = [dmg_type_str_map[dtype] for dtype in self.dmg_types]
        spec_strs = [spec.name for spec in self.specials]
        spec_strs = ["-"] if len(spec_strs) == 0 else spec_strs
        return "<{} {}gp {}d{} {}x{} {}ft {}lb. {} {} >".format(
            self.weapon_type.name, self.cost, self.num_dice, self.num_side,
            self.crit_range, self.crit_dmg, self.weapon_range,
            self.weight, ",".join(dmg_types), ",".join(spec_strs))

