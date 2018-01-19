
from .base_feats import Feat,Proficiency,FeatType
from .feats_st import SpellFocus
from model.entity.armor import ArmorType
from model.entity.living.spells import SpellSchool


class Unseat(Feat):

    ability_scores = [(Ability.str, 13)]
    skill_ranks = [(SkillName.ride, 1)]
    feats = {MountedCombat(), PowerAttack(), ImprovedBullRush()}
    base_attack_bonus = 1
    short_desc = "Knock opponents from their mounts"
    feat_type = FeatType.combat


class VitalStrike(Feat):

    base_attack_bonus = 6
    short_desc = "Deal twice the normal damage on a single attack"
    feat_type = FeatType.combat


class WeaponFinesse(Feat):

    short_desc = "Use Dex instead of Str on attack rolls with light weapons"
    feat_type = FeatType.combat


class WeaponFocus(Feat):

    proficient_with_subset = True
    base_attack_bonus = 1
    short_desc = "+1 bonus on attack rolls with one weapon"
    feat_type = FeatType.combat

    def __init__(self):
        super().__init__(ArmorType.medium_armor)


class WeaponSpecialization(Feat):

    # TODO
    short_desc = "+2 bonus on damage rolls with one weapon"
    feat_type = FeatType.combat


class WhirlwindAttack(Feat):

    # TODO
    short_desc = "Make one melee attack against all foes within reach"
    feat_type = FeatType.combat


class WidenSpell(Feat):

    # TODO
    short_desc = ""
    feat_type = FeatType.metamagic


class WindStance(Feat):

    # TODO
    short_desc = ""
    feat_type = FeatType.combat

