
from enum import unique, Enum

from model.entity.living.size import Size,SizeBonus
from model.entity.living.ability_scores import Ability
from model.entity.living.skills import Skill, SkillName, SkillBonus
from model.entity.weapons import WeaponType
from model.bonuses import Bonus,BonusReason,BonusType


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

        con = Bonus(btype=BonusType.ability, amt=2, reason=BonusReason.race)
        con.subtype = Ability.con

        wis = Bonus(btype=BonusType.ability, amt=2, reason=BonusReason.race)
        wis.subtype = Ability.wis

        cha = Bonus(btype=BonusType.ability, amt=-2, reason=BonusReason.race)
        cha.subtype = Ability.cha

        self.bonuses = [con, wis, cha]
        self.proficiencies = {WeaponType.battleaxe, WeaponType.heavy_pick,
            WeaponType.warhammer}
        # NOTE: treat anything dwarven as a martial weapon
        #   WeaponType.dwarven_waraxe, WeaponType.dwarven_urgrosh


class Elf(Race):

    name = RaceName.elf

    def __init__(self):

        self.size = Size.medium

        dex = Bonus(btype=BonusType.ability, amt=2, reason=BonusReason.race)
        dex.subtype = Ability.dex

        ab_int = Bonus(btype=BonusType.ability, amt=2, reason=BonusReason.race)
        ab_int.subtype = Ability.int

        con = Bonus(btype=BonusType.ability, amt=-2, reason=BonusReason.race)
        con.subtype = Ability.con

        self.bonuses = [dex, ab_int, con]

        self.proficiencies = {WeaponType.longbow, WeaponType.composite_longbow,
            WeaponType.longsword, WeaponType.rapier, WeaponType.shortbow,
            WeaponType.composite_shortbow}
        # NOTE: treat anything elven as a martial weapon
        #   WeaponType.elven_curve_blade


class Gnome(Race):

    name = RaceName.gnome

    def __init__(self):
        self.size = Size.small

        con = Bonus(btype=BonusType.ability, amt=2, reason=BonusReason.race)
        con.subtype = Ability.con

        cha = Bonus(btype=BonusType.ability, amt=2, reason=BonusReason.race)
        cha.subtype = Ability.cha

        ab_str = Bonus(btype=BonusType.ability, amt=-2, reason=BonusReason.race)
        ab_str.subtype = Ability.str

        self.bonuses = [con, cha, ab_str]

        self.proficiencies = set()
        # NOTE: treat anything gnome as a martial weapon
        #   WeaponType.gnome_hooked_hammer


class HalfElf(Race):

    name = RaceName.half_elf

    def __init__(self, ability_bonus):
        self.size = Size.medium
        self.bonuses = [ability_bonus,
                        ]
        self.proficiencies = set()


class HalfOrc(Race):

    name = RaceName.half_orc

    def __init__(self, ability_bonus):
        self.size = Size.medium
        self.bonuses = [ability_bonus]
        self.proficiencies = {WeaponType.greataxe, WeaponType.falchion}
        # NOTE: treat anything orc as martial
        #   WeaponType.orc_double_axe


class Halfling(Race):

    name = RaceName.halfling

    def __init__(self):
        self.size = Size.small

        dex = Bonus(btype=BonusType.ability, amt=2, reason=BonusReason.race)
        dex.subtype = Ability.dex

        cha = Bonus(btype=BonusType.ability, amt=2, reason=BonusReason.race)
        cha.subtype = Ability.cha

        ab_str = Bonus(btype=BonusType.ability, amt=2, reason=BonusReason.race)
        ab_str.subtype = Ability.cha

        self.bonuses = [dex, cha, ab_str,
                        SkillBonus(SkillName.stealth, 4, BonusReason.race),
                        ]

        self.proficiencies = {WeaponType.sling}
        # NOTE: Treat anything halfling as martial weapon
        #   WeaponType.halfling_sling_staff


class Human(Race):

    name = RaceName.human

    def __init__(self, ability_bonus):
        self.size = Size.medium
        self.bonuses = [ability_bonus]
        self.proficiencies = set()

