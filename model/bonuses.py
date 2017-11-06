
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


BonusType = Enum("BonusType", [
    "ability",
    "ac",
    "attack",
    "damage",
    "init",
    "skill",
    "size",
    "movement",
])


class Bonus():

    def __init__(self, btype=None, amt=None, reason=None, conds=None,
                    subtype=None):
        # this will handle the simple bonuses that add some kind
        # of modifier to a value
        self.type = btype
        self.amount = amt
        self.reason = reason
        self.conditions = set()
        self.subtype = subtype

    def __repr__(self):
        subtype = self.subtype.name if self.subtype else ""
        return "<Bonus:{} {} {} {}>".format(self.type.name, self.amount,
            self.reason.name, subtype)

