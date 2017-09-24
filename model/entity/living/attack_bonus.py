
from copy import copy

from model.bonuses import *
from model.entity.classes.util import ClassName


class HandAttackBonus():

    def __init__(self):
        self.total = 0
        self.bonuses = set()

    def add_bonus(self, bonus):
        self.bonuses.add(bonus)
        self.calculate_total()

    def remove_bonus(self, bonus):
        self.bonuses.remove(bonus)
        self.calculate_total()

    def calculate_total(self):
        self.total = 0
        for bonus in self.bonuses:
            self.total += bonus.amount

    def clear(self):
        self.bonuses.clear()
        self.total = 0

    def __repr__(self):
        return "<HandAttackBonus: {}>".format(self.total)


class BaseAttackBonus():

    def __init__(self):
        self.total = []
        self.bonuses = set()
        self.class_babs = []
        self.main_hand = HandAttackBonus()
        self.off_hand = HandAttackBonus()

    def add_bonus(self, bonus, main_hand=True, off_hand=False):
        #TODO apply bonuses to main/off hand
        if bonus.reason == BonusReason.entity_class:
            self.class_babs.append(bonus)
        else:
            self.bonuses.add(bonus)
        self.calculate_total()

    def remove_bonus(self, bonus):
        if bonus in self.bonuses:
            self.bonuses.remove(bonus)
            self.calculate_total()

    def calculate_total(self):
        # first, determine individual bonuses
        total = 0
        for bonus in self.bonuses:
            total += bonus.amount

        # second, determine class_babs
        babs = [bab.amount for bab in self.class_babs]
        if len(babs) > 1:
            babs.reverse()
            total_babs = copy(babs[0])
            for bab in babs[1:]:
                for i in range(len(bab)):
                    total_babs[i] += bab[i]
        elif len(babs) == 1:
            total_babs = babs[0]
        else:
            total_babs = [0]
        
        self.total = [class_bonus+total for class_bonus in total_babs]

    def __repr__(self):
        return "<BaseAttackBonus: {}>".format(self.total)


class AttackBonus(Bonus):

    def __init__(self, amt, reason):
        self.amount = amt
        self.reason = reason

    def __repr__(self):
        return "<AttackBonus {} - {}>".format(self.amount, self.reason.name)

