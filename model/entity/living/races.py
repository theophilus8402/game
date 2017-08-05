
from enum import unique, Enum

from model.entity.living.ability_scores import Ability, AbilityBonus
from model.entity.living.skills import Skill, SkillName, SkillBonus
from model.bonuses import BonusReason


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


class Race():

    def __init__(self):
        pass


class Dwarf(Race):

    def __init__(self):
        self.bonuses = [AbilityBonus(Ability.con, 2, BonusReason.race),
                        AbilityBonus(Ability.wis, 2, BonusReason.race),
                        AbilityBonus(Ability.cha, -2, BonusReason.race),
                        ]
        self.size = Size.medium


class Elf(Race):

    def __init__(self):
        self.bonuses = [AbilityBonus(Ability.dex, 2, BonusReason.race),
                        AbilityBonus(Ability.int, 2, BonusReason.race),
                        AbilityBonus(Ability.con, -2, BonusReason.race),
                        ]
        self.size = Size.medium


class Gnome(Race):

    def __init__(self):
        self.bonuses = [AbilityBonus(Ability.con, 2, BonusReason.race),
                        AbilityBonus(Ability.cha, 2, BonusReason.race),
                        AbilityBonus(Ability.str, -2, BonusReason.race),
                        ]
        self.size = Size.small


class HalfElf(Race):

    def __init__(self, ability_bonus):
        self.bonuses = [ability_bonus]
        self.size = Size.medium


class HalfOrc(Race):

    def __init__(self, ability_bonus):
        self.bonuses = [ability_bonus]
        self.size = Size.medium


class Halfling(Race):

    def __init__(self):
        self.bonuses = [
            AbilityBonus(Ability.dex, 2, BonusReason.race),
            AbilityBonus(Ability.cha, 2, BonusReason.race),
            AbilityBonus(Ability.str, -2, BonusReason.race),
            SkillBonus(SkillName.stealth, 4, BonusReason.race),
            ]
        self.size = Size.small


class Human(Race):

    def __init__(self, ability_bonus):
        self.bonuses = [ability_bonus]
        self.size = Size.medium

