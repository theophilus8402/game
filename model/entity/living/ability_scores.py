
import enum
from math import floor

from model.bonuses import Bonus, BonusReason


@enum.unique
class Ability(enum.Enum):
    str = 0
    dex = 1
    con = 2
    wis = 3
    int = 4
    cha = 5


class AbilityScore():

    def __init__(self, ability, score):
        self.ability = ability
        self.base_score = score
        self.total = score
        self.bonuses = []
        self.modifier = AbilityBonus(ability, 0, BonusReason.ability_modifier)
        self.calculate_modifier()

    def add_bonus(self, bonus):
        # adds the bonus (could be +/-)
        # the bonus will have some kind of identifier + the numerical bonus + reason
        # updates the modifier
        # TODO: should probably do some checks to see if the bonus cannot be added
        self.bonuses.append(bonus)
        self.total += bonus.amount
        self.calculate_modifier()

    def remove_bonus(self, bonus):
        # removes the bonus
        # the bonus will have some kind of identifier + the numerical bonus
        # Updates the modifier
        if bonus in self.bonuses:
            self.bonuses.remove(bonus)
            self.total -= bonus.amount
            self.calculate_modifier()

    def calculate_modifier(self):
        # (total - 10)/2
        self.modifier.amount = floor((self.total - 10)/2)

    def __repr__(self):
        sign = "+" if self.modifier.amount > 0 else ""
        return "<{} {}, {}{}>".format(self.ability, self.total, sign,
            self.modifier.amount)


class AbilityBonus(Bonus):

    def __init__(self, ability, amt, reason):
        self.type = ability
        self.amount = amt
        self.reason = reason

    def __repr__(self):
        sign = "+" if self.amount > 0 else ""
        return "<{} {}{}>".format(self.type, sign, self.amount)


class TwoHandedBonus(AbilityBonus):

    def __init__(self, ability_modifier):
        self.orig_modifier = ability_modifier

    @property
    def amount(self):
        return self.orig_modifier.amount * 1.5

