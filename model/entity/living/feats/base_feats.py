
from enum import Enum

FeatRequirement = Enum("FeatRequirement", [
    "channel_energy",
    "proficient",
])

class Feat():

    # prerequisites
    # ability_scores = [(dex, 13), (int, 15)]
    ability_scores = []
    base_attack_bonus = 0
    # skill_ranks = [(stealth, 1), (slight_of_hand, 23)]
    skill_ranks = []
    feats = []
    caster_level = 0

    short_desc = "some feat"
    long_desc = "some longer feat description"

    def __repr__(self):
        reqs = "---"
        return "<{} {} {}>".format(self.__class__.__name__, reqs, self.short_desc)
