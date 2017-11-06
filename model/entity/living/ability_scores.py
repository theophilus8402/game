
from enum import unique,Enum
from math import floor

from model.bonuses import Bonus, BonusReason


Ability = Enum("Ability", [
    "str",
    "dex",
    "con",
    "wis",
    "int",
    "cha",
])


class AbilityScore():

    def __init__(self, ability, score):
        self.ability = ability
        self.base_score = score
        self.total = score
        self.bonuses = []
        self.modifier = 0
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
        self.modifier = floor((self.total - 10)/2)

    def __repr__(self):
        sign = "+" if self.modifier > 0 else ""
        return "<{} {}, {}{}>".format(self.ability.name, self.total, sign,
            self.modifier)

