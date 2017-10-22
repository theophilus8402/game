
from collections import defaultdict

from model.bonuses import BonusReason
from model.entity.basic_entity import Entity
from model.entity.classes.util import ClassName, class_name_map
from model.entity.classes.fighter import Fighter
from model.entity.classes.wizard import Wizard
from model.entity.damage import DmgType
from model.entity.living.ability_scores import Ability, AbilityScore, AbilityBonus
from model.entity.living.armor_class import ArmorClass
from model.entity.living.attack_bonus import BaseAttackBonus, AttackBonus
from model.entity.living.status_effects import *
from model.entity.inventory import Inventory
from model.entity.living.equip import HumanoidEquipment
from model.entity.living.skills import *
from model.entity.living.size import SizeBonus,get_size_modifier,size_modifier_map
from model.entity.living.equip import possible_equipment_slots, EqSlots
from model.entity.living.races import Human
from model.entity.living.round_info import RoundInfo
from model.entity.inventory import Inventory
from model.entity.damage import DmgInfo
from model.entity.weapons import Weapon,UnarmedStrike,WeaponCategory
from model.info import Status
from model.util import roll, RollType, RollInfo


CMDS_BASIC_MOVEMENT = {"n", "ne", "e", "se", "s", "sw", "w", "nw"}
CMDS_BASIC_ATTACK = {"hit", "fhit", "cast"}
CMDS_BASIC_HUMANOID = {"get", "eat", "drink", "wear", "wield", "remove",
    "unwield", "l", "look", "lh", "quit", "exit", "say"}
CMDS_DEBUG = {}


class Living(Entity):

    def __init__(self, ab_scores=None, race=None, class_name=ClassName.fighter):
        self.total_xp = 0
        self.name = ""
        self.base_attack_bonus = BaseAttackBonus()
        if not ab_scores:
            ab_scores = [
                AbilityScore(Ability.str, 10),
                AbilityScore(Ability.dex, 10),
                AbilityScore(Ability.con, 10),
                AbilityScore(Ability.wis, 10),
                AbilityScore(Ability.int, 10),
                AbilityScore(Ability.cha, 10),
            ]
        self.set_ability_scores(ab_scores)
        self.skills = {}
        self.initialize_skills()

        self.proficiencies = set()

        self.ac = ArmorClass()
        dex_mod = self.ability_scores[Ability.dex].modifier
        self.ac.add_bonus(dex_mod)

        if not race:
            ability_bonus = AbilityBonus(AbilityName.str, 2, BonusReason.race)
            race = Human(ability_bonus)
        self.set_race(race)

        self.classes = []
        self.add_level(class_name)
        self.equipment = HumanoidEquipment()
        self.inventory = Inventory()
        self.cur_hp = 10
        self.sneaking = 0

    def __repr__(self):
        classes_str = ",".join(["{}:{}".format(ctype.name.name, ctype.level) for ctype in self.classes])
        return "<{} - {} / {}>".format(self.name, self.race.name.name, classes_str)

    def set_ability_scores(self, ability_scores):
        self.ability_scores = {}
        for ability_score in ability_scores:
            self.ability_scores[ability_score.ability] = ability_score

    def set_race(self, race):
        for bonus in race.bonuses:
            self.add_bonus(bonus)
        self.race = race
        self.size_modifier = get_size_modifier(self.race.size)

        # proficiencies
        self.proficiencies = self.proficiencies.union(race.proficiencies)

        # add size_modifier to things affected by size
        self.base_attack_bonus.add_bonus(self.size_modifier)
        self.ac.add_bonus(self.size_modifier)

        self.set_size(self.race.size)

    def set_size(self, size):
        self.size = size
        self.size_modifier.amount = size_modifier_map[size]

        # update values that are affected by size
        self.base_attack_bonus.calculate_total()
        self.ac.calculate_total()

    def add_class(self, class_name):
        class_type = class_name_map[class_name]()
        self.classes.append(class_type)

        for bonus in class_type.bonuses:
            self.add_bonus(bonus)

        self.base_attack_bonus.add_bonus(class_type.class_bab)

        self.proficiencies = self.proficiencies.union(class_type.proficiencies)

    def is_proficient(self, weapon_type):
        for class_ in self.classes:
            if weapon_type in class_.proficiencies:
                return True
        if weapon_type in self.race.proficiencies:
            return True
        # couldn't find the proficiency
        return False

    def add_bonus(self, bonus):
        if isinstance(bonus, AbilityBonus):
            self.ability_scores[bonus.type].add_bonus(bonus)
        elif isinstance(bonus, SkillBonus):
            self.skills[bonus.type].add_bonus(bonus)
        elif isinstance(bonus, AttackBonus):
            self.base_attack_bonus.add_bonus(bonus)
        elif isinstance(bonus, SizeBonus):
            self.base_attack_bonus.add_bonus(bonus)
            self.ac.add_bonus(bonus)

    def add_level(self, class_name):
        found_class = False
        for class_type in self.classes:
            if class_type.name == class_name:
                class_type.level_up()
                found_class = True
                break
        if not found_class:
            self.add_class(class_name)

        # recalculate things that might have changed by the level up
        self.base_attack_bonus.calculate_total()

    def initialize_skills(self):
        for skill_name in SkillName:
            ability = skill_ability_map[skill_name]["ability"]
            ability_bonus = self.ability_scores[ability].modifier
            self.skills[skill_name] = Skill(skill_name, ability_bonus)

    def skill_check(self, skill_name):
        return RollInfo(1, 20, bonuses=self.skills[skill_name].bonuses)

    def roll_attack(self, full_hit=False, main_hand=True):
        mresults = []
        oresults = []

        bonuses = self.base_attack_bonus.bonuses
        if full_hit == True:
            # do a full hit for main_hand
            hbonus = self.base_attack_bonus.main_hand.total
            for att_bonus in self.base_attack_bonus.total:
                mresults.append(RollInfo(1, 20, flat_bonus=att_bonus+hbonus))

            # do a full hit for off hand
            obonus = self.base_attack_bonus.off_hand.total
            # TODO: determine how many off hand attacks to do

        elif main_hand == True:
            # roll for just the first main_hand attack
            hbonus = self.base_attack_bonus.main_hand.total
            first_bonus = self.base_attack_bonus.total[0]
            mresults.append(RollInfo(1, 20, flat_bonus=first_bonus+hbonus))

        return (mresults, oresults)

    def apply_damage(self, dmg_info):
        # Get's DmgInfo with dmg_types and amounts set
        # Applies all appropriate dmg resistances
        # Applies final dmg to entity

        if DmgType.healing in dmg_info._orig_dmg.keys():
            # heal the person!
            # TODO: may need to determine if the person should be hurt by healing
            self.cur_hp += dmg_info.total
        else:
            self.cur_hp -= dmg_info.total

    def roll_damage(self, main_hand=True):

        # find the weapon
        hand_slot = EqSlots.right_hand if main_hand else EqSlots.left_hand
        weapon = self.equipment[hand_slot]
        if not weapon:
            weapon = UnarmedStrike(self.size)

        # TODO: determine dmg modifiers
        dmg_bonus = 1

        # roll damage
        dice = weapon.num_dice
        sides = weapon.num_side
        roll_result = RollInfo(dice, sides, flat_bonus=dmg_bonus)

        # dmg type
        # TODO: for now just return the first dmg type we see on the weapon
        dmg_type = weapon.dmg_types[0]

        dmg_info = DmgInfo()
        dmg_info.add_dmg(dmg_type, roll_result.total)

        return dmg_info

    @property
    def xp_to_give(self):
        # Returns the amount of xp to give to it's killers
        # TODO: give a better amt than this static value
        return 100

    def gain_xp(self, xp_amt):
        # Add xp to the entity
        # Return True if the entity gains a level
        #   False otherwise
        gained_level = False
        self.total_xp += xp_amt

        # TODO: Determine if they gained a level
        return gained_level

    def sneak(self, hide=True):
        if hide:
            result = self.skill_check(SkillName.stealth)
        else:
            # just want to return a RollInfo even though it's useless
            result = RollInfo(0, 0, [])
        self.sneaking = result.total
        return result

    def get_feat_bonuses(self, item):
        # Returns a list of attack/dmg bonuses based on feat related to the item
        feat_bonuses = []

        # check if proficient
        if not self.is_proficient(item.weapon_type):
            reason = BonusReason.not_weapon_proficient
            bonus = AttackBonus(amt=-4, reason=reason)
            feat_bonuses.append(bonus)

        # check for weapon focuses
        #TODO

        return feat_bonuses

    def get_ability_bonuses(self, item):
        # Returns a list of attack/dmg bonuses based on ability_modifiers
        ability_bonuses = []

        # Notes:
        #   one_handed melee could be wielded w/ two hands
        #       it would get 1.5 dmg bonus from str
        #   two_handed_melee will get 1.5 dmg bonus
        #   light_melee can be wielded two handed but just get's 1x str
        #   thrown weapons get str bonus
        #   ranged weapons get no str bonus if positive
        #       but, they can lose points based on -str modifier
        #       composite bows change this how
        #   normally, all melee attack bonuses are based on str
        #       however, weapon finesse can change this to dex
        #       there's a limited set of weapons that can be used in this way

        # check to see if it's ranged or melee/thrown
        if item.category in [WeaponCategory.light_melee,
            WeaponCategory.one_handed_melee]:
            # melee/thrown usually uses str
            # TODO: check to see if should use dex w/ weapon_finess
            str_mod = self.ability_scores[Ability.str].modifier
            ability_bonuses.append(str_mod)
        elif item.category == WeaponCategory.two_handed_melee:
            str_mod = self.ability_scores[Ability.str].modifier

            # should use two handed str bonus 1.5
            two_handed_mod = TwoHandedBonus(str_mod)
            ability_bonuses.append(two_handed_mod)
        else:
            # ranged/ray usually uses dex
            pass

        return ability_bonuses

    def equip(self, item, eqslot):
        # make sure the item is in the inventory
        if item not in self.inventory:
            return Status.item_not_in_inventory

        # make sure the eqslot is valid and empty
        if eqslot not in self.equipment.allowed_eq_slots:
            return Status.invalid_eq_slot

        if self.equipment[eqslot] is not None:
            return Status.eqslot_not_free

        # TODO: make sure entity is physically healthy enough

        # equip the item!
        # remove the item from the inventory
        self.inventory.remove(item)

        # add the item to the equipment slot
        self.equipment[eqslot] = item

        # deal with all the bonuses and what not by equiping the item
        if isinstance(item, Weapon):
            if eqslot == EqSlots.right_hand:
                hand_bonuses = self.base_attack_bonus.main_hand
            else:
                hand_bonuses = self.base_attack_bonus.off_hand

            # get feat attack bonuses
            bonuses = self.get_feat_bonuses(item)

            # get bonuses based on ability modifiers
            bonuses.extend(self.get_ability_bonuses(item))

            for bonus in bonuses:
                if (isinstance(bonus, AbilityBonus) or
                    isinstance(bonus, AttackBonus)):
                    hand_bonuses.add_bonus(bonus)
                else:
                    print("Have a bonus I'm not handling while equiping: ")
                    print(bonus)
                    self.add_bonus(bonus)
            
        return Status.all_good

    def unequip(self, thing_to_unequip):
        if isinstance(thing_to_unequip, EqSlots):
            eqslot = thing_to_unequip
            # make sure there's an item in the eqslot
            item = self.equipment[eqslot]
            if item is None:
                return Status.eqslot_empty

        elif isinstance(thing_to_unequip, Entity):
            item = thing_to_unequip
            # make sure the item is in the equipment
            if item not in self.equipment:
                return Status.item_not_in_equipment

            # find the corresponding eqslot
            for slot, eq_item in self.equipment.items():
                if item is eq_item:
                    eqslot = slot
                    break

        else:
            # nothing specified so, bale nicely?
            return Status.all_good

        # make sure there's room in the inventory to receive the item
        can_add = self.inventory.can_add_item(item)
        if can_add is not Status.all_good:
            return can_add

        # remove the item in the eqslot
        del self.equipment[eqslot]

        # remove the bonuses associated with it
        if isinstance(item, Weapon):
            if eqslot == EqSlots.right_hand:
                self.base_attack_bonus.main_hand.clear()
            elif eqslot == EqSlots.left_hand:
                self.base_attack_bonus.off_hand.clear()
        
        # add the item to the inventory
        self.inventory.add_item(item)

        return Status.all_good

    def meets_feat_reqs(self, feat):
        # checks requirements of feat
        # if entity satisfies requirements, returns True
        # False otherwise

        # check ability_scores
        for ab,score in feat.ability_scores:
            if score > self.ability_scores[ab]:
                return False

        # check base attack bonus
        if feat.base_attack_bonus:
            # assuming base_attack_bonus is going solely off class bab's
            babs = [cbab[0] for cbab in self.base_attack_bonus.class_babs]
            if feat.base_attack_bonus > sum(class_babs):
                return False

        # check skill ranks
        for skill,rank in feat.skill_ranks:
            if rank > self.skills[skill].total:
                return False

        # check feats
        if feat.feats:
            if not set(feat.feats).issubset(self.feats):
                return False

        # check caster level
        if feat.caster_level or feat.arcane_caster_level:
            caster_level = 0
            arcane_caster_level = 0
            for eclass in self.classes:
                # divine spell classes
                if eclass.name in [ClassName.cleric, ClassName.druid,
                    ClassName.paladin, ClassName.ranger]:
                    caster_level += eclass.level
                elif eclass.name in [ClassName.bard, ClassName.sorcerer,
                    ClassName.wizard]:
                    arcane_caster_level += eclass.level
            caster_level += arcane_caster_level

            if feat.caster_level > caster_level:
                return False
            if feat.arcane_caster_level > arcane_caster_level:
                return False

        # check channel energy
        if feat.channel_energy:
            class_names = set([eclass.name for eclass in self.classes])
            if class_names.isdisjoint({ClassName.cleric, ClassName.paladin}):
                return False

        # check proficiencies
        if not self.proficiencies(feat.proficiencies):
            return False

        return True


