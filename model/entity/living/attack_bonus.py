
from collections import defaultdict
from copy import copy

from model.bonuses import *
from model.entity.classes.util import ClassName,get_bab
from model.entity.living.equip import EqSlots
from model.entity.living.size import get_size_attack_bonus


class AttackBonusHandler():

    def __init__(self):
        self.clear()

    def clear(self):
        # this should show _all_ attack bonuses
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
        if len(babs) < 1:
            return []
        babs.sort(key=len, reverse=True)
        bab_len = len(babs[0])

        final_bab = []
        for i in range(bab_len):
            final_bab.append(sum([bab[i] for bab in babs if i < len(bab)]))
        return final_bab


def calculate_attack_bonuses(self):

        bonus_handler = self.attack_bonus

        bonus_handler.clear()

        # size
        bonus_handler.bonuses.append(get_size_attack_bonus(self.size))

        # TODO: spell effects

        # class babs
        for _class in self.classes:
            name = _class.name
            bonus_handler.babs[name] = get_bab(name, _class.level)

        # TODO: feats
        # feat_attack_bonuses = []
        # for feat in self.feats:
        #   feat_attack_bonuses.extend([bonus for bonus in feat.bonuses if bonus == att])

        # hands
        for slot,hand_bonuses in [
                (EqSlots.right_hand, bonus_handler.main_hand_bonuses),
                (EqSlots.left_hand, bonus_handler.off_hand_bonuses)]:

            # find the weapon
            weapon = self.equipment[slot]
            if not weapon:
                # TODO: gotta figure out how to use hands as weapons
                #   probably go with actually having an "item" for hands
                continue

            # proficient
            if not self.is_proficient(weapon.weapon_type):
                penalty = AttackBonus(-4, BonusReason.not_weapon_proficient)
                hand_bonuses.append(penalty)
            
            # ability modifier
            hand_bonuses.append(self.get_ability_attack_bonus(weapon))

            # TODO: feats
            # TODO: item bonuses

        self.attack_bonus.calculate()

