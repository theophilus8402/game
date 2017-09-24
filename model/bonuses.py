
from enum import unique, Enum

BonusReason = Enum("BonusReason", [
    "race",
    "entity_class",
    "trained_skill",
    "trained_class_skill",
    "ability_modifier",
    "size",
    "spell_bless",
    "base_armor_class",
    "armor_bonus",
    "not_weapon_proficient",
])


class Bonus():

    def __init__(self):
        # this will handle the simple bonuses that add some kind
        # of modifier to a value
        self.type = None
        self.amount = None
        self.reason = None

