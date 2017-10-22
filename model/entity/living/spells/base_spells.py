
from enum import Enum

SpellSchool = Enum("SpellSchool", [
    "abjuration",
    "conjuration",
    "divination",
    "enchantment",
    "evocation",
    "illusion",
    "necromancy",
    "transmutation",
])


SpellName = Enum("SpellName", [
    "cure_light_wounds",
])

spell_map = {}

