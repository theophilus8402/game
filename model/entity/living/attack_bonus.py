
from copy import copy

from model.bonuses import *
from model.entity.classes.util import ClassName


class BaseAttackBonus():

    def __init__(self):
        self.total = []
        self.bonuses = []
        self.class_babs = []
        self.main_hand = self.total
        self.off_hand = self.total

    def add_bonus(self, bonus, main_hand=True, off_hand=False):
        #TODO apply bonuses to main/off hand
        if bonus.reason == BonusReason.entity_class:
            self.class_babs.append(bonus)
        else:
            self.bonuses.append(bonus)
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
        # TODO fix main_hand and off_hand calculations
        self.main_hand = self.total
        self.off_hand = self.total

    def __repr__(self):
        return "<BaseAttackBonus: {}>".format(self.total)


class AttackBonus(Bonus):

    def __init__(self, amt, reason):
        self.amount = amt
        self.reason = reason

    def __repr__(self):
        return "<AttackBonus {} - {}>".format(self.amount, self.reason.name)

