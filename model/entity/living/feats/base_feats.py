
from enum import Enum


class Feat():

    # prerequisites
    # ability_scores = [(dex, 13), (int, 15)]
    ability_scores = []
    base_attack_bonus = 0
    # skill_ranks = [(stealth, 1), (slight_of_hand, 23)]
    skill_ranks = []
    feats = set()
    caster_level = 0
    arcane_caster_level = 0
    channel_energy = False
    proficiencies = set()

    short_desc = "some feat"
    long_desc = "some longer feat description"

    def __init__(self):
        self.subset = None

    def __repr__(self):
        reqs = "---"
        return "<{} {} {}>".format(self.__class__.__name__, reqs, self.short_desc)

    def __hash__(self):
        return hash((self.__class__, self.subset))

    def __eq__(self, other_feat):
        return ((self.subset == other_feat.subset) and
            isinstance(other_feat, self.__class__))
