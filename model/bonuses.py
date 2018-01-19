
from enum import unique, Enum

BonusReason = Enum("BonusReason", [
    "race",
    "entity_class",
    "class_bab",
    "trained_skill",
    "trained_class_skill",
    "base_ability_score",
    "ability_modifier",
    "size",
    "spell_bless",
    "base_armor_class",
    "armor",
    "not_weapon_proficient",
    "master_work",
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


Conditional = Enum("Conditional", [
    "main_hand",
    "off_hand",
])


class Bonus():

    def __init__(self, btype=None, amt=None, reason=None, conds=set(),
                    subtype=None, eqslot=None):
        # this will handle the simple bonuses that add some kind
        # of modifier to a value
        self.type = btype
        self.amount = amt
        self.reason = reason
        self.conditions = conds
        self.subtype = subtype

    def __repr__(self):
        subtype = self.subtype.name if self.subtype else ""
        return "<Bonus:{} {} {} {}>".format(self.type.name, self.amount,
            self.reason.name, subtype)


class AbilityBonus(Bonus):

    # this is to increase the ability score not to document modifiers

    def __init__(self, amt=None, reason=None, conds=set(), subtype=None):
        super().__init__(btype=BonusType.ability, amt=amt, reason=reason,
                            conds=conds, subtype=subtype)


class ACBonus(Bonus):

    def __init__(self, amt=None, reason=None, conds=set(), subtype=None):
        super().__init__(btype=BonusType.ac, amt=amt, reason=reason,
                            conds=conds, subtype=subtype)


class AttackBonus(Bonus):

    def __init__(self, amt=None, reason=None, conds=set(), subtype=None,
                    eqslot=None):
        super().__init__(btype=BonusType.attack, amt=amt, reason=reason,
                            conds=conds, subtype=subtype)


class DamageBonus(Bonus):

    def __init__(self, amt=None, reason=None, conds=set(), subtype=None):
        super().__init__(btype=BonusType.damage, amt=amt, reason=reason,
                            conds=conds, subtype=subtype)


class InitBonus(Bonus):

    def __init__(self, amt=None, reason=None, conds=set(), subtype=None):
        super().__init__(btype=BonusType.init, amt=amt, reason=reason,
                            conds=conds, subtype=subtype)


class SkillBonus(Bonus):

    def __init__(self, amt=None, reason=None, conds=set(), subtype=None):
        super().__init__(btype=BonusType.skill, amt=amt, reason=reason,
                            conds=conds, subtype=subtype)


class SizeBonus(Bonus):

    def __init__(self, amt=None, reason=None, conds=set(), subtype=None):
        super().__init__(btype=BonusType.size, amt=amt, reason=reason,
                            conds=conds, subtype=subtype)


class MovementBonus(Bonus):

    def __init__(self, amt=None, reason=None, conds=set(), subtype=None):
        super().__init__(btype=BonusType.movement, amt=amt, reason=reason,
                            conds=conds, subtype=subtype)


