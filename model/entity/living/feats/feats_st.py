
from .base_feats import Feat


class SpellFocus(Feat):

    short_desc = "+1 bonus on save DCs for one school"

    def __init__(self, school):
        self.subset = school

