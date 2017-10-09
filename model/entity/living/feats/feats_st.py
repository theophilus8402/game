
from .base_feats import Feat,Proficiency


class SpellFocus(Feat):

    short_desc = "+1 bonus on save DCs for one school"

    def __init__(self, school):
        self.subset = school


class ShieldProficiency(Proficiency):

    short_desc = "No penalties on attack rolls when using a shield"

