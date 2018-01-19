
from enum import unique, Enum

from model.entity.classes import ClassName
from model.entity.living.living import Living
from model.entity.living.races import Race,RaceName
from model.entity.living.size import Size
from model.entity.living.ability_scores import Ability,AbilityScore
from model.entity.living.skills import Skill,SkillName
from model.entity.weapons import WeaponType,simple_weapon_group
from model.entity.armor import ArmorType
from model.bonuses import Bonus,BonusReason,BonusType,SkillBonus


class Goblin(Race):

    name = RaceName.goblin

    def __init__(self):
        self.size = Size.small

        # speed 30ft (fast)
        # darkvision up to 60ft
        # +4 racial bonus to ride, stealth
        racial_ride_bonus = SkillBonus(4, BonusReason.race,
            subtype=SkillName.ride)
        racial_stealth_bonus = SkillBonus(4, BonusReason.race,
            subtype=SkillName.stealth)
        # 4 ranks in ride, 0 ranks in stealth, 4 ranks in swim
        ride_rank = SkillBonus(4, BonusReason.trained_skill,
            subtype=SkillName.ride)
        swim_rank = SkillBonus(4, BonusReason.trained_skill,
            subtype=SkillName.swim)
        # feats: improved_initiative

        self.bonuses = [racial_ride_bonus, racial_stealth_bonus, ride_rank,
            swim_rank]
        self.proficiencies = {WeaponType.short_sword, *simple_weapon_group, 
            ArmorType.light_armor, ArmorType.shield}

def make_goblin():
    ability_scores = [
        AbilityScore(Ability.str, 11),
        AbilityScore(Ability.dex, 15),
        AbilityScore(Ability.con, 12),
        AbilityScore(Ability.wis, 9),
        AbilityScore(Ability.int, 10),
        AbilityScore(Ability.cha, 6),
        ]

    goblin = Living(ab_scores=ability_scores, race=Goblin(),
        class_name=ClassName.monster)
    goblin.name = "Gobby"
    goblin.symbol = "g"

    return goblin

    # Base Atk +1; CMB +0; CMD 12
    # Feats Improved Initiative
    # Skills Ride +10, Stealth +10, Swim +4
    # Racial Modifiers +4 Ride, +4 Stealth
    # Languages Goblin

