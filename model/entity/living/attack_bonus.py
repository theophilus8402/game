
from collections import defaultdict
from copy import copy

from model.bonuses import *
from model.entity.classes.util import ClassName
from model.entity.living.size import get_size_attack_bonus


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


class AttackBonusHandler():

    def __init__(self):
        self.clear()

    def clear(self):
        self.bonuses = []
        self.babs = {}
        self.off_hand_babs = []
        self.main_hand_bonuses = []
        self.off_hand_bonuses = []
        self.main_hand_total = []
        self.off_hand_total = []

    def calculate(self):
        normal_bonus = sum([bonus.amount for bonus in self.bonuses])

        # class babs added together
        babs = self._calculate_babs()

        # main_hand bonuses
        main_hand = sum([bonus.amount for bonus in self.main_hand_bonuses])
        main_hand += normal_bonus
        self.main_hand_total = [main_hand+bab for bab in babs]

        # off_hand bonuses
        off_hand = sum([bonus.amount for bonus in self.off_hand_bonuses])
        off_hand += normal_bonus
        self.off_hand_total = [off_hand+bab for bab in babs]

    def _calculate_babs(self):

        # find max bab len
        babs = list(self.babs.values())
        if len(babs) <= 1:
            return []
        babs.sort(key=len, reverse=True)
        bab_len = len(babs[0])

        final_bab = []
        for i in range(bab_len):
            final_bab.append(sum([bab[i] for bab in babs if i < len(bab)]))
        return final_bab

        """
        final_babs = []
        for i in range(bab_len):
            final_babs[i] = sum([bab[i] for bab in babs])

        return final_babs
        """


def calculate_attack_bonuses(self):

        bonus_handler = self.attack_bonus

        bonus_handler.clear()

        # size
        bonus_handler.bonuses.append(get_size_attack_bonus(self.size))

        # spell effects
        # class babs
        # feats
        # hands
        #   proficient
        #   feats
        #   ability modifier
        #   item bonuses

