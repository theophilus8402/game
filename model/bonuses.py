
from enum import unique, Enum

@unique
class BonusReason(Enum):
    race = 0
    entity_class = 1


class Bonus():

    def __init__(self):
        # this will handle the simple bonuses that add some kind
        # of modifier to a value
        self.type = None
        self.amount = None
        self.reason = None

