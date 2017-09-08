
from enum import unique, Enum

from model.entity.living.size import Size,SizeBonus
from model.entity.living.ability_scores import Ability, AbilityBonus
from model.entity.living.skills import Skill, SkillName, SkillBonus
from model.bonuses import BonusReason


@unique
class RaceName(Enum):
    dwarf = 1
    elf = 2
    gnome = 3
    half_elf = 4
    half_orc = 5
    halfling = 6
    human = 7


class Race():

    def __init__(self):
        pass

    def __repr__(self):
        return "<race: {}>".format(self.name.name)


class Dwarf(Race):

    name = RaceName.dwarf

    def __init__(self):
        self.size = Size.medium
        self.bonuses = [AbilityBonus(Ability.con, 2, BonusReason.race),
                        AbilityBonus(Ability.wis, 2, BonusReason.race),
                        AbilityBonus(Ability.cha, -2, BonusReason.race),
                        ]


class Elf(Race):

    name = RaceName.elf

    def __init__(self):
        self.size = Size.medium
        self.bonuses = [AbilityBonus(Ability.dex, 2, BonusReason.race),
                        AbilityBonus(Ability.int, 2, BonusReason.race),
                        AbilityBonus(Ability.con, -2, BonusReason.race),
                        ]


class Gnome(Race):

    name = RaceName.gnome

    def __init__(self):
        self.size = Size.small
        self.bonuses = [AbilityBonus(Ability.con, 2, BonusReason.race),
                        AbilityBonus(Ability.cha, 2, BonusReason.race),
                        AbilityBonus(Ability.str, -2, BonusReason.race),
                        ]


class HalfElf(Race):

    name = RaceName.half_elf

    def __init__(self, ability_bonus):
        self.size = Size.medium
        self.bonuses = [ability_bonus,
                        ]


class HalfOrc(Race):

    name = RaceName.half_orc

    def __init__(self, ability_bonus):
        self.size = Size.medium
        self.bonuses = [ability_bonus,
                        ]


class Halfling(Race):

    name = RaceName.halfling

    def __init__(self):
        self.size = Size.small
        self.bonuses = [AbilityBonus(Ability.dex, 2, BonusReason.race),
                        AbilityBonus(Ability.cha, 2, BonusReason.race),
                        AbilityBonus(Ability.str, -2, BonusReason.race),
                        SkillBonus(SkillName.stealth, 4, BonusReason.race),
                        ]


class Human(Race):

    name = RaceName.human

    def __init__(self, ability_bonus):
        self.size = Size.medium
        self.bonuses = [ability_bonus,
                        ]

