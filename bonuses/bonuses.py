
from enum import Enum
from math import floor

from model.bonuses import *
from model.entity.living.ability_scores import Ability


class Living():

    def __init__(self):
        # this bonuses will not keep track of any unique bonuses
        # it will be a combination of all the other bonuses

        self.effects = SpellEffects()
        self.equipment = Equipment()
        self.feats = Feats()
        self.skills = Skills()
        self.ability_scores = AbilityScores()

    @property
    def bonuses(self):
        _bonuses = [*self.effects.bonuses,
                    *self.equipment.bonuses,
                    *self.feats.bonuses,
                    *self.skills.bonuses,
                    *self.ability_scores.bonuses,
                    ]
        return _bonuses

    def get_bonuses(self, bonus_type, conds=set(), subtype=None):
        bonuses = [bonus for bonus in self.bonuses
                            if ((bonus.type == bonus_type) and
                                bonus.conditions.issubset(conds))]
        if subtype:
            bonuses = [bonus for bonus in bonuses if bonus.subtype == subtype]
        return bonuses

    def set_max_dex_bonus(self):
        # looks to see if there's armor that limits the max dex bonus
        # if no limit, set's the max dex bonus to -1
        max_dex_bonus = -1

        armor = self.equipment.get("torso")
        if armor:
            max_dex_bonus = armor.max_dex_bonus

        self.ability_scores.max_dex_bonus = max_dex_bonus

    def calculate_ability_scores(self):

        # go through bonuses to figure out what's the total ability score
        scores = self.ability_scores.scores
        for ab in Ability:
            score = sum([bonus.amount for bonus in self.get_bonuses(
                            BonusType.ability, subtype=ab)])
            modifier = floor((score - 10)/2)
            scores[ab] = (score, modifier)

    def equip(self, item, slot):
        self.equipment.equiped[slot] = item
        self.calculate_ability_scores()


Race = Enum("Race", [
    "human",
    "halfling",
])


Class = Enum("Class", [
    "fighter",
    "wizard",
])


class Equipment():

    def __init__(self):
        # this will not hold any unique bonuses
        # it will simply hold the combined bonuses from all items equiped
        # maybe I can make this a property or setter that automatically
        # gathers the bonuses from the items equiped

        self.equiped = {}

    @property
    def bonuses(self):
        _bonuses = [bon for item in self.equiped.values()
                            for bon in item.bonuses]
        return _bonuses


class Weapon():

    def __init__(self):
        # attack bonuses will be conditional based on the hand that equiped it
        self.bonuses = []


class Armor():

    def __init__(self):
        self.bonuses = []


class SpellEffects():

    def __init__(self):
        self.effects = []

    @property
    def bonuses(self):
        _bonuses = [bon for effect in self.effects
                            for bon in effect.bonuses]
        return _bonuses


class SpellEffect():

    def __init__(self):
        self.bonuses = []


class Feat():

    def __init__(self):
        self.bonuses = []


class Feats():

    # Feats stores all the different feats

    def __init__(self):
        self.bonuses = []


class Skills():

    # Skills stores all the different skills

    def __init__(self):
        # this doesn't store unique bonuses
        self.bonuses = []


class Skill():

    def __init__(self):
        # bonuses store here are class bonuses and rank bonuses
        # if an item or spell effect or something like that relate to a skill
        # they will be stored with the item/spell effect and NOT in here
        # the larger entity class will pick up the appropriate skill bonuses
        self.bonuses = []


class AbilityScores():

    def __init__(self):

        # these are base scores
        # they can go up when leveling
        # but bonuses based on items and spells will not show here
        self.base_scores = []

        # these will be the total score, living_entity will have to set them
        # because it needs to get the bonuses from other places
        self.scores = {}

        # these modifiers should reflect the most up-to-date scores
        # these are the bonuses that other skills, attacks, ac... will use
        self.modifier_bonuses = []

    @property
    def bonuses(self):
        # these are the combined bonuses
        return [*self.base_scores, *self.modifier_bonuses]

    def calculate_bonuses(self):
        # this should be called after the living entity's
        # self.calculate_ability_scores()

        # this will calculate modifiers, set them, and then create
        # bonuses for all other things that will need bonuses
        # these bonuses will be things like Skill bonuses, attack bonuses...

        mods = {key : val[1] for key,val in self.scores.items()}

        #####
        # calculate modifiers
        #####

        # ac
        # TODO: figure out max dex bonus
        ac = ACBonus(mods[Ability.dex], BonusReason.ability_modifier)
        self.modifier_bonuses.append(ac)

        # attack bonuses... we'll go ahead and calculate all the different ones
        # str based
        # TODO: use conds to help determine which attack bonus to use
        str_att = AttackBonus(mods[Ability.str], BonusReason.ability_modifier,
                    conds=set())
        self.modifier_bonuses.append(str_att)
        # dex based
        # TODO: use conds to help determine which attack bonus to use
        dex_att = AttackBonus(mods[Ability.dex], BonusReason.ability_modifier,
                    conds=set())
        self.modifier_bonuses.append(dex_att)

        # skill bonuses
        #self.bonuses.append(SkillBonus(


if __name__ == "__main__":

    mdagger = Weapon()
    mdagger.bonuses.append(AttackBonus(1, BonusReason.master_work, conds={Conditional.main_hand}))

    spiffy_armor = Armor()
    spiffy_armor.bonuses.append(ACBonus(5, BonusReason.armor))
    spiffy_armor.bonuses.append(AbilityBonus(3, BonusReason.armor,
                                        subtype=Ability.str))

    bob = Living()
    bob.equip(mdagger, "main_hand")
    bob.equip(spiffy_armor, "torso")

    blessing = SpellEffect()
    blessing.bonuses.append(AttackBonus(1, BonusReason.spell_bless))
    blessing.bonuses.append(ACBonus(1, BonusReason.spell_bless))

    bob.effects.effects.append(blessing)

    ab_str = AbilityBonus(14, BonusReason.base_ability_score,
                            subtype=Ability.str)
    ab_con = AbilityBonus(12, BonusReason.base_ability_score,
                            subtype=Ability.con)
    ab_dex = AbilityBonus(13, BonusReason.base_ability_score,
                            subtype=Ability.dex)
    ab_int = AbilityBonus(11, BonusReason.base_ability_score,
                            subtype=Ability.int)
    ab_wis = AbilityBonus(14, BonusReason.base_ability_score,
                            subtype=Ability.wis)
    ab_cha = AbilityBonus(8, BonusReason.base_ability_score,
                            subtype=Ability.cha)
    bob.ability_scores.base_scores.append(ab_str)
    bob.ability_scores.base_scores.append(ab_con)
    bob.ability_scores.base_scores.append(ab_dex)
    bob.ability_scores.base_scores.append(ab_int)
    bob.ability_scores.base_scores.append(ab_wis)
    bob.ability_scores.base_scores.append(ab_cha)
    bob.calculate_ability_scores()
    bob.ability_scores.calculate_bonuses()

# setup = "from __main__ import bob,BonusType"
# timeit("bob.get_bonuses(BonusType.attack, {})", setup=setup)

