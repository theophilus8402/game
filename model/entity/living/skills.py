
import enum

from model.bonuses import Bonus, BonusReason
from model.entity.living.ability_scores import Ability

SkillName = enum.Enum("SkillName", [
    "acrobatics",
    "appraise",
    "bluff", 
    "climb", 
    "craft", 
    "diplomacy", 
    "disable_device", 
    "disguise", 
    "escape_artist",
    "fly",
    "handle_animal",
    "heal",
    "intimidate",
    "knowledge_arcana",
    "knowledge_dungeoneering",
    "knowledge_engineering",
    "knowledge_geography",
    "knowledge_history",
    "knowledge_local",
    "knowledge_nature",
    "knowledge_nobility",
    "knowledge_planes",
    "knowledge_religion",
    "linguistics",
    "perception",
    "perform",
    "profession",
    "ride",
    "sense_motive",
    "sleight_of_hand",
    "spellcraft",
    "stealth",
    "survival",
    "swim",
    "use_magic_device",
])


skill_ability_map = {
    SkillName.acrobatics : {"untrained": True, "ability": Ability.dex},
    SkillName.appraise : {"untrained": True, "ability": Ability.int},
    SkillName.bluff : {"untrained": True, "ability": Ability.cha},
    SkillName.climb : {"untrained": True, "ability": Ability.str},
    SkillName.craft : {"untrained": True, "ability": Ability.int},
    SkillName.diplomacy : {"untrained": True, "ability": Ability.cha},
    SkillName.disable_device : {"untrained": False, "ability": Ability.dex},
    SkillName.disguise : {"untrained": True, "ability": Ability.cha},
    SkillName.escape_artist : {"untrained": True, "ability": Ability.dex},
    SkillName.fly : {"untrained": True, "ability": Ability.dex},
    SkillName.handle_animal : {"untrained": False, "ability": Ability.cha},
    SkillName.heal : {"untrained": True, "ability": Ability.wis},
    SkillName.intimidate : {"untrained": True, "ability": Ability.cha},
    SkillName.knowledge_arcana : {"untrained": False, "ability": Ability.int},
    SkillName.knowledge_dungeoneering : {"untrained": False, "ability": Ability.int},
    SkillName.knowledge_engineering : {"untrained": False, "ability": Ability.int},
    SkillName.knowledge_geography : {"untrained": False, "ability": Ability.int},
    SkillName.knowledge_history : {"untrained": False, "ability": Ability.int},
    SkillName.knowledge_local : {"untrained": False, "ability": Ability.int},
    SkillName.knowledge_nature : {"untrained": False, "ability": Ability.int},
    SkillName.knowledge_nobility : {"untrained": False, "ability": Ability.int},
    SkillName.knowledge_planes : {"untrained": False, "ability": Ability.int},
    SkillName.knowledge_religion : {"untrained": False, "ability": Ability.int},
    SkillName.linguistics : {"untrained": False, "ability": Ability.int},
    SkillName.perception : {"untrained": True, "ability": Ability.wis},
    SkillName.perform : {"untrained": True, "ability": Ability.cha},
    SkillName.profession : {"untrained": False, "ability": Ability.wis},
    SkillName.ride : {"untrained": True, "ability": Ability.dex},
    SkillName.sense_motive : {"untrained": True, "ability": Ability.wis},
    SkillName.sleight_of_hand : {"untrained": False, "ability": Ability.dex},
    SkillName.spellcraft : {"untrained": False, "ability": Ability.int},
    SkillName.stealth : {"untrained": True, "ability": Ability.dex},
    SkillName.survival : {"untrained": True, "ability": Ability.wis},
    SkillName.swim : {"untrained": True, "ability": Ability.str},
    SkillName.use_magic_device : {"untrained": False, "ability": Ability.cha},
}


class Skill():

    def __init__(self, skill, ability_modifier):
        self.skill = skill
        # total will be the total not including circumstantial bonuses
        self.total = 0
        self.class_skill = False
        self.bonuses = [ability_modifier]
        self.circumstantial_bonuses = []
        self.calculate_total()

    def set_class_skill(self, class_skill):
        # sets class_skill to true or false
        self.class_skill = class_skill
        self.calculate_total()

    def calculate_total(self):
        # this will not count circumstantial bonuses
        # this will not return anything
        # it will set re-calculate the skill total
        # this will not test to see if the bonus is allowed
        total = 0
        found_trained_skill = False
        found_trained_class_skill = False
        for bonus in self.bonuses:
            total += bonus.amount
            if bonus.reason == BonusReason.trained_skill:
                found_trained_skill = True
            elif bonus.reason == BonusReason.trained_class_skill:
                found_trained_class_skill = True
        if self.class_skill and found_trained_skill and not found_trained_class_skill:
            new_bonus = SkillBonus(self.skill, 3,
                BonusReason.trained_class_skill)
            self.add_bonus(new_bonus)
        self.total = total

    def add_bonus(self, bonus):
        #TODO: add checks to make sure we can add the bonus
        self.bonuses.append(bonus)
        self.calculate_total()

    def remove_bonus(self, bonus=None, bonus_reason=None):
        # remove the bonus if it was in the list
        if bonus and (bonus in self.bonuses):
            self.bonuses.remove(bonus)

        elif bonus_reason:
            saved_bonuses = [bonus for bonus in self.bonuses
                                if bonus.reason != bonus_reason]
            self.bonuses = saved_bonuses

        self.calculate_total()

    def __repr__(self):
        return "<{}: {}>".format(self.skill.name, self.total)


