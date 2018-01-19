
from enum import unique,Enum

from model.bonuses import Bonus,ACBonus,AttackBonus,SkillBonus,BonusReason
from model.entity.living.skills import SkillName

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

def get_size_stealth_bonus(size):
    return SkillBonus(size_modifier_map[size]*4, BonusReason.size,
        subtype=SkillName.stealth)

def get_size_ac_bonus(size):
    return ACBonus(size_modifier_map[size], BonusReason.size)

def get_size_attack_bonus(size):
    return AttackBonus(size_modifier_map[size], BonusReason.size)


