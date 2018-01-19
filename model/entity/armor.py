#!/usr/bin/python3

from enum import Enum,unique

from model.bonuses import ACBonus,BonusReason
from model.entity.basic_entity import Entity
from model.entity.living.size import Size
from model.entity.living.equip import EqSlots

MAX_DEX_BONUS = 10

ArmorType = Enum("ArmorType", [
    "spiked_armor",
    "light_armor",
    "medium_armor",
    "heavy_armor",
    "shield",
    "tower_shield",
])


ArmorName = Enum("ArmorName", [
    "padded",
    "leather",
    "studded_leather",
    "chain_shirt",
    "hide",
    "scale_mail",
    "chainmail",
    "breastplate",
    "splint_mail",
    "banded_mail",
    "half_plate",
    "full_plate",
    "buckler",
    "light_wooden_shield",
    "light_steel_shield",
    "heavy_wooden_shield",
    "heavy_steel_shield",
    "tower_shield",
])


# Basic armor:
class Armor(Entity):

    def __init__(self, name=ArmorName.padded, atype=ArmorType.light_armor, 
                    cost=5, ac_bonus=1, mdex=MAX_DEX_BONUS, ac_penalty=2,
                    sp_fail=10, speed=30, weight=10):
        super().__init__()
        self.name = name.name if isinstance(name, ArmorName) else name
        self.armor_type = atype
        self.base_cost = cost
        self.armor_bonus = ACBonus(amt=ac_bonus, reason=BonusReason.armor_bonus)
        self.max_dex_bonus = mdex
        self.armor_check_penalty = ac_penalty
        self.arcane_spell_fail = sp_fail
        self.speed = speed
        self.weight=weight
        self.bonuses = []

        if self.armor_type in {ArmorType.light_armor, ArmorType.medium_armor,
                                ArmorType.heavy_armor}:
            self.eqslot = EqSlots.torso
        elif self.armor_type in {ArmorType.shield, ArmorType.tower_shield}:
            self.eqslot = EqSlots.left_hand

    def __repr__(self):
        return "<{name} {cost} {ac}/{mdex} {pen} {fail} {spd} {lb}lbs>".format(
            name=self.name, cost=self.base_cost, ac=self.armor_bonus.amount,
            mdex=self.max_dex_bonus, pen=self.armor_check_penalty,
            fail=self.arcane_spell_fail, spd=self.speed, lb=self.weight)
            


class Padded(Armor):

    def __init__(self, size=Size.medium):
        if size == Size.small:
            speed = 20
        elif size == Size.medium:
            speed = 30
        super().__init__(ArmorName.padded, ArmorType.light_armor,
            5, 1, 8, 0, 5, speed, 10)

class Leather(Armor):

    def __init__(self, size=Size.medium):
        if size == Size.small:
            speed = 20
        elif size == Size.medium:
            speed = 30
        super().__init__(ArmorName.leather, ArmorType.light_armor,
            10, 2, 6, 0, 10, speed, 15)

class StuddedLeather(Armor):

    def __init__(self, size=Size.medium):
        if size == Size.small:
            speed = 20
        elif size == Size.medium:
            speed = 30
        super().__init__(ArmorName.padded, ArmorType.light_armor,
            5, 1, 8, 0, 5, speed, 10)

class Padded(Armor):

    def __init__(self, size=Size.medium):
        if size == Size.small:
            speed = 20
        elif size == Size.medium:
            speed = 30
        super().__init__(ArmorName.padded, ArmorType.light_armor,
            5, 1, 8, 0, 5, speed, 10)


class LightWoodenShield(Armor):

    def __init__(self, size=Size.medium):
        super().__init__(ArmorName.light_wooden_shield, ArmorType.shield,
            3, 1, MAX_DEX_BONUS, -1, 5, 30, 5)


