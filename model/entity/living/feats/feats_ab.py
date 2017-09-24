
from . base_feats import Feat,FeatRequirement
from model.entity.armor import ArmorType

class Acrobatic(Feat):

    short_desc = "+2 bonus on Acrobatics and Fly checks"


class AgileManeuvers(Feat):

    short_desc = "Use your Dex bonus when calculating your CMB"


class Alertness(Feat):

    short_desc = "+2 bonus on Perception and Sense Motive checks"


class AlignmentChannel(Feat):

    specials = [FeatRequirement.channel_energy]
    short_desc = "Channel energy can heal or harm outsiders"


class AnimalAffinity(Feat):

    short_desc = "+2 bonus on Handle Animal and Ride checks"


class ArcaneArmorTraining(Feat):

    proficiencies = [ArmorType.light_armor]
    caster_level = 3
    short_desc = "Reduce your arcane spell failure chance by 10%"


class ArcaneArmorMastery(Feat):

    proficiencies = [ArmorType.medium_armor]
    caster_level = 7
    short_desc = "Reduce your arcane spell failure chance by 20%"

