
from model.bonuses import Bonus,BonusReason
from model.entity.living.ability_scores import Ability,AbilityBonus

class ArmorClass():

    def __init__(self):
        self.bonuses = [ArmorBonus(10, BonusReason.base_armor_class)]

    def __repr__(self):
        return "<AC: {}/{}>".format(self.total, self.flat_footed)

    def add_bonus(self, bonus):
        self.bonuses.append(bonus)
        self.calculate_total()

    def calculate_total(self):
        total = 0
        dex_bonus = 0
        for bonus in self.bonuses:
            if isinstance(bonus, AbilityBonus) and (bonus.type == Ability.dex):
                dex_bonus = bonus.amount
            else:
                total += bonus.amount
        self.total = total + dex_bonus
        self.flat_footed = total


class ArmorBonus(Bonus):

    def __init__(self, amt, reason):
        self.amount = amt
        self.reason = reason

    def __repr__(self):
        sign = "+" if self.amount > 0 else ""
        return "<{} {}{}>".format(self.reason.name, sign, self.amount)

