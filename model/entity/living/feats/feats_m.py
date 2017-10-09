
from .base_feats import Feat,Proficiency


class MartialWeaponProficiency(Proficiency):

    short_desc = "No penalty on attacks made with one martial weapon"

    def __init__(self, proficiency):
        super().__init__(proficiency)

