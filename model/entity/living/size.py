
from enum import unique,Enum

from model.bonuses import Bonus,BonusReason

@unique
class Size(Enum):
    fine = -4
    diminutive = -3
    tiny = -2
    small = -1
    medium = 0
    large = 1
    huge = 2
    gargantuan = 3
    colossal = 4


size_modifier_map = {
    Size.colossal : -8,
    Size.gargantuan : -4,
    Size.huge : -2,
    Size.large : -1,
    Size.medium : 0,
    Size.small : 1,
    Size.tiny : 2,
    Size.diminutive : 4,
    Size.fine : 8,
}

def get_size_modifier(size):
    return SizeBonus(size_modifier_map[size], BonusReason.size)


class SizeBonus(Bonus):

    def __init__(self, amt, reason):
        self.amount = amt
        self.reason = reason

    def __repr__(self):
        sign = "+" if self.amount > 0 else ""
        return "<SizeBonus:{} {}{}>".format(self.reason.name, sign, self.amount)


