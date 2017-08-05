
from enum import unique, Enum

BonusReason = Enum("BonusReason", [
    "race",
    "entity_class",
    "trained_skill",
    "trained_class_skill",
    "ability_modifier",
])


class Bonus():

    def __init__(self):
        # this will handle the simple bonuses that add some kind
        # of modifier to a value
        self.type = None
        self.amount = None
        self.reason = None

