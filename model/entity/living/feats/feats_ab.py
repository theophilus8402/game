
from .base_feats import Feat
from .feats_st import SpellFocus
from model.entity.armor import ArmorType
from model.entity.living.spells import SpellSchool

class Acrobatic(Feat):

    short_desc = "+2 bonus on Acrobatics and Fly checks"


class AgileManeuvers(Feat):

    short_desc = "Use your Dex bonus when calculating your CMB"


class Alertness(Feat):

    short_desc = "+2 bonus on Perception and Sense Motive checks"


class AlignmentChannel(Feat):

    channel_energy = True
    short_desc = "Channel energy can heal or harm outsiders"


class AnimalAffinity(Feat):

    short_desc = "+2 bonus on Handle Animal and Ride checks"


class ArcaneArmorTraining(Feat):

    proficiencies = {ArmorType.light_armor}
    caster_level = 3
    short_desc = "Reduce your arcane spell failure chance by 10%"


class ArcaneArmorMastery(Feat):

    proficiencies = {ArmorType.medium_armor}
    caster_level = 7
    short_desc = "Reduce your arcane spell failure chance by 20%"


class ArcaneStrike(Feat):

    arcane_caster_level = 1
    short_desc = "+1 damage and weapons are considered magic"


class ArmorProficiencyLight(Feat):

    short_desc = "No penalties on attack rolls while wearing light armor"


class ArmorProficiencyMedium(Feat):

    proficiencies = {ArmorType.light_armor}
    short_desc = "No penalties on attack rolls while wearing medium armor"


class ArmorProficiencyHeavy(Feat):

    proficiencies = {ArmorType.medium_armor}
    short_desc = "No penalties on attack rolls while wearing heavy armor"


class Athletic(Feat):

    short_desc = "+2 bonus on Climb and Swim checks"


class AugmentSummoning(Feat):

    feats = {SpellFocus(SpellSchool.conjuration)}
    short_desc = "Summoned creatures gain +4 Str and Con"
