
from copy import copy

from model.bonuses import Bonus,BonusReason,ACBonus
from model.entity.armor import Armor
from model.entity.living.ability_scores import Ability
from model.entity.living.equip import EqSlots

class ArmorClass():

    def __init__(self):
        self.base_armor_class = ACBonus(10, BonusReason.base_armor_class)
        self.armor_bonus = ACBonus(0, BonusReason.armor_bonus)
        self.shield_bonus = ACBonus(0, BonusReason.armor_bonus)
        self.dex_bonus = ACBonus(0, BonusReason.ability_modifier)
        self.bonuses = []
        self.total = 0
        self.flat_footed = 0
        self.touch = 0

    def __repr__(self):
        return "<AC: {} F:{} T:{}>".format(self.total, self.flat_footed,
                    self.touch)

    def clear(self):
        self.bonuses.clear()
        self.calculate_total()

    def add_bonus(self, bonus):
        self.bonuses.append(bonus)
        self.calculate_total()

    def calculate_total(self):
        bonus_amt = sum([bonus.amount for bonus in self.bonuses])
        base_amt = bonus_amt + self.base_armor_class.amount
        armor_amt = self.armor_bonus.amount + self.shield_bonus.amount
        dex_amt = self.dex_bonus.amount

        # total is everything
        self.total = base_amt + armor_amt + dex_amt

        # flat_footed is armor but no dex
        self.flat_footed = base_amt + armor_amt

        # touch is dex but no armor
        self.touch = base_amt + dex_amt


def calculate_ac(self):

    armor = self.equipment[EqSlots.torso]
    if armor:
        max_dex_bonus = copy(armor.max_dex_bonus)
        self.ac.armor_bonus = copy(armor.armor_bonus)
    else:
        max_dex_bonus = 8

    # TODO: right now, I'm assuming shields are in the left hand
    shield = self.equipment[EqSlots.left_hand]
    if shield and isinstance(shield, Armor):
        max_dex_bonus = min(max_dex_bonus, shield.max_dex_bonus)
        self.ac.shield_bonus = copy(shield.armor_bonus)

    # get dex bonus
    dex_mod = self.ability_scores[Ability.dex].modifier
    dex_mod = min(dex_mod, max_dex_bonus)
    self.ac.dex_bonus = ACBonus(dex_mod, BonusReason.ability_modifier)

    # go through all equip'd items for AC bonus
    # go through all feats for bonuses
    # go through race/class stuff?
    # get size bonus

