
from entities import Entity

weapon_category = ["simple", "martial", "exotic"]
subtype = ["unarmed", "light_melee", "one_handed_melee", "two_handed_melee",
            "ranged"]
dmg_type = ["slashing", "piercing", "blunt"]

class Weapon(Entity):

    def __init__(self, name, category, subtype, cost, dmg, crit, range,
                    weight, dmg_type, special, bonuses, id=None):
        super().__init__(name, id)

        self.category = category
        self.subtype = subtype
        self.cost = cost
        self.small_dmg, self.medium_dmg = dmg
        self.crit = crit
        self.range = range
        self.weight = weight
        self.dmg_type = dmg_type
        self.special = special
        self.bonuses = bonuses

def make_shortsword():
    return Weapon("shortsword", "martial", "light_melee", 10, 
                    ("1d4", "1d6"), (19, 2), 0, 2, "piercing", None, [])

def make_longsword():
    return Weapon("longsword", "martial", "one_handed_melee", 15, 
                    ("1d6", "1d8"), (19, 2), 0, 4, "slashing", None, [])

def make_longbow():
    return Weapon("longbow", "martial", "ranged", 75, 
                    ("1d6", "1d8"), (20, 3), 100, 3, "piercing", None, [])

shortsword = make_shortsword()
longsword = make_longsword()
longbow = make_longbow()

