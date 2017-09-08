
from collections import defaultdict

from model.bonuses import BonusReason
from model.entity.basic_entity import Entity
from model.entity.classes.util import ClassName, class_name_map
from model.entity.classes.fighter import Fighter
from model.entity.classes.wizard import Wizard
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
from model.info import Status
from model.util import roll, RollType, RollInfo


CMDS_BASIC_MOVEMENT = {"n", "ne", "e", "se", "s", "sw", "w", "nw"}
CMDS_BASIC_ATTACK = {"hit", "fhit", "cast"}
CMDS_BASIC_HUMANOID = {"get", "eat", "drink", "wear", "wield", "remove",
    "unwield", "l", "look", "lh", "quit", "exit", "say"}
CMDS_DEBUG = {}


def add_status_msg(entity, msg):
    entity.status_msgs.add(msg)


def remove_status_msg(entity, msg):
    try:
        entity.status_msgs.remove(msg)
    except:
        pass    # I don't think I want to do anything...


def get_attack_bonus(src_ent, melee=True, range_pen=0):
    """
    att_bonus = base_att_bonus + ability_mod + size_mod + misc
    we'll do the d20 roll somehwere else
    This will return a list of attack bonuses
    """

    if melee:
        attribute = "str"
    else:
        attribute = "dex"
    attrib, ability_mod = src_ent.attrib[attribute]

    #size_mod = model.util.size_modifiers[src_ent.size]
    misc_attack_bonus, misc_list = src_ent.attack_bonus["misc"]

    attack_bonus_list = []
    for base_attack_bonus in src_ent.attack_bonus["base"]:
        # attack_bonus (melee) = base_attack_bonus + str_mod + size_mod
        attack_bonus = (base_attack_bonus + ability_mod + size_mod 
            + misc_attack_bonus)
        # attack_bonus (ranged) = base_attack_bonus + dex_mod + size_mod
        # + range_penalty
        if not melee:
            attack_bonus += range_pen

        attack_bonus_list.append(attack_bonus)

    return attack_bonus_list


def get_roll_possibilities(entity, eqslot=None, defence=False):
    roll_possibs = defaultdict(lambda: 0)

    # determine if we attack or defence info from the entity
    if defence is False:
        poss_types = {RollType.critical_miss, RollType.miss, RollType.hit,
            RollType.critical_hit}
    else:
        poss_types = {RollType.dodge, RollType.block}

    # see if we need to get info from a wielded item
    if eqslot in {EqSlots.right_hand, EqSlots.left_hand}:
        item = entity.equipment[eqslot]
    else:
        item = None

    # add up the possibilities
    for poss_type in poss_types:
        roll_possibs[poss_type] += entity.race.possibilities.get(poss_type, 0)
        roll_possibs[poss_type] += entity.class_type.possibilities.get(poss_type, 0)
        roll_possibs[poss_type] += entity.equipment.possibilities.get(poss_type, 0)

        if item:
            roll_possibs[poss_type] += item.possibilities.get(poss_type, 0)

    return roll_possibs


def check_successful_attack(src_ent, dst_ent, info=None):
    #TODO: actually implement this
    return True


def determine_weapon_dmg(entity, weapon):
    """
    Returns amount of damage based on item in eqslot
    """
    dmg_info = DmgInfo()

    # TODO: include strength bonus

    results = weapon.get_damage()
    for dmg_type, amt in results.items():
        dmg_info.add_dmg(dmg_type, amt)

    return dmg_info


class Living(Entity):

    def __init__(self, ab_scores=None, race=None, class_name=ClassName.fighter):
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

        self.ac = ArmorClass()
        dex_mod = self.ability_scores[Ability.dex].modifier
        self.ac.add_bonus(dex_mod)

        if not race:
            ability_bonus = AbilityBonus(AbilityName.str, 2, BonusReason.race)
            race = Human(ability_bonus)
        self.set_race(race)

        self.classes = []
        self.add_class(class_name)
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
        results = []

        if full_hit == True:
            # do a full hit for main_hand
            for att_bonus in self.base_attack_bonus.main_hand:
                results.append(RollInfo(1, 20, flat_bonus=att_bonus))
        elif main_hand == True:
            # roll for just the first main_hand attack
            fbonus = self.base_attack_bonus.main_hand[0]
            results.append(RollInfo(1, 20, flat_bonus=fbonus))
        else:
            # roll attack roll for just off-hand
            pass

        return results

    def sneak(self, hide=True):
        if hide:
            result = self.skill_check(SkillName.stealth)
        else:
            # just want to return a RollInfo even though it's useless
            result = RollInfo(0, 0, [])
        self.sneaking = result.total
        return result

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

        return Status.all_good

    def unequip(self, eqslot=None, item=None):
        if eqslot is not None:
            # make sure there's an item in the eqslot
            item = self.equipment[eqslot]
            if item is None:
                return Status.eqslot_empty

        elif item is not None:
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
        
        # add the item to the inventory
        self.inventory.add_item(item)

        return Status.all_good


