
from collections import defaultdict

import model.util
from model.entity.basic_entity import Entity
from model.entity.living.status_effects import *
from model.entity.living.equip import possible_equipment_slots
from model.entity.living.round_info import RoundInfo
from model.entity.inventory import Inventory
from model.info import Status


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

    size_mod = model.util.size_modifiers[src_ent.size]
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


def get_attack_roll_possibilities(person):
    attack_info = defaultdict(lambda: 0)
    # Get critical_miss, miss, hit, critical_hit info from person
    # get race info
    for attack_type, value in person.race.attack_possibilities.items():
        attack_info[attack_type] += value

    # get class info
    for attack_type, value in person.class_type.attack_possibilities.items():
        attack_info[attack_type] += value

    # get equipment info
    # we'll do this somewhere else?
    #for attack_type, value in weapon.attack_possibilities:
    #    attack_info[attack_type] += value

    # get status info (spells, physical ailments)

    return attack_info


def get_defence_roll_possibilities(person):
    def_info = defaultdict(lambda: 0)

    # Get critical_miss, miss, hit, critical_hit info from person
    # get race defences
    for def_type, value in person.race.defence_possibilities.items():
        def_info[def_type] += value

    # class info
    for def_type, value in person.class_type.defence_possibilities.items():
        def_info[def_type] += value

    # get equipment info
    for def_type, value in person.equipment.defence_possibilities.items():
        def_info[def_type] += value
    
    return def_info


def check_successful_attack(src_ent, dst_ent, info=None):
    #TODO: actually implement this
    return True


def determine_weapon_dmg(src_ent, dst_ent):
    """
    dmg will be returned as a negative number to indicate that health
    should be subtracted from target.
    """
    #TODO: actually implement this
    dmg = -6
    return dmg


class NewLiving():

    def __init__(self):
        self.race = None
        self.class_type = None
        self.equipment = None   #TODO: change this because the eq slots depends
                                # on the race (different arms...)
        self.inventory = None
        self.stats = {
            "str": 0,
            "dex": 0,
            "con": 0,
            "wis": 0,
            "int": 0,
            "cha": 0,
        }

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


# Basic living:
class Living(Entity):

    def __init__(self):
        Entity.__init__(self)
        self.equipment = {slot: None for slot in possible_equipment_slots}
        self.type = "living"      # the different entity classes
        self.pclass = "fighter"
        self.cur_mp = 0
        self.max_mp = 10
        self.status_msgs = set()
        self.visual_range = 5
        self.level = 0
        self.hit_dice = "2d4"
        self.race = "creature"

        self.blob_state = None

        self.max_num_attacks = 1
        self.main_hand = Body.right_arm
        self.round_info = RoundInfo()

        # new
        self.status_effects = set()

        self.abilities = {}
        self.fortitude = {
            "total": 0,
            "base": 0,
            "magic": 0,
            "tmp": 0 }
        self.reflex = {
            "total": 0,
            "base": 0,
            "magic": 0,
            "tmp": 0 }
        self.will = {
            "total": 0,
            "base": 0,
            "magic": 0,
            "tmp": 0 }
        self.alignment = "neutral good"
        self.diety = "none"
        self.size = "medium"
        self.age = 21
        self.gender = "male"
        self.height = "6'2\""
        self.subdual_msg = 0
        self.arcane_spell_failure = 0
        self.armour_check_penalty = -4
        self.speed = 20
        self.ac = 10
        """{
        #AC = 10 + armour bonus + shield bonus + dex mod + size mod + other
            "total": 0,
            "base": 10,
            "armour": 0,
            "shield": 0,
            "misc": (0, None),  # first num will be the total, then []
                                #   of things that give the att bonus
            }
        """
        self.eq = {
            Body.right_arm  : None,
            Body.left_arm   : None,
            Body.torso      : None,
            Body.head       : None,
            }
        self.skills = []
        self.spells = []
        self.feats = []
        self.ammunition = []
        self.inventory = Inventory()
        self.lift = {
            "over_head": 200,
            "off_ground": 600,
            "push_drag": 1000 }
        self.carrying = 0   # how much weight we are carrying
                            #   this will include items wielded and eq
                            # this will only be modified when we pick
                            #   stuff up or when we drop it
                            # we may have to modify it when we cast a
                            #   feather spell on something...
        self.carry_max = 0
        self.exp = 0
        self.money = 10

    def drop_item(self, item):
        # check to make sure the item is in the inventory or being wielded
        #   won't drop worn items... must remove them first
        # "drop" the item
        #   add the item to the tile's entity list
        #   remove the weight from self.carrying
        #   item.carried_by = None
        #   set the item's current location
        #   remove the item from our inventory/wielded stuff
        pass

    def set_attrib(self, name, value):
        mod = math.floor((value - 10) / 2)
        self.attrib[name] = (value, mod)

    def can_move(self):
        can_move = True
        required_parts = {Body.left_leg, Body.right_leg}
        status = check_health(self, required_parts)
        if status:
            can_move = False
        return (can_move, status)

    #TODO: I think I'm gonna get rid of mp and have some kind of time thing
    def change_mp(self, mp_delta):
        self.cur_mp += mp_delta
        if self.cur_mp > self.max_mp:
            self.cur_mp = self.max_mp

    def wield(self, hand, item):
        status = 0
        """
        hand = "{}_hand".format(hand)
        if self.eq.get(hand) is None:
            # there's nothing in that hand, so we can go ahead and wield it
            self.eq[hand] = item
            # need to check if the item even has an attack bonus
            if hasattr(item, "attack_bonus"):
                self.add_attack_bonus(item)
            # check to see if it has an AC bonus
            if hasattr(item, "armour_bonus") and \
                (item.armour_bonus is not None):
                # currently, I'm assuming shield are the only thing you
                #   can wield that will give AC bonus
                self.add_armour_bonus("shield", item.armour_bonus)
        else:
            status = 4  # you already have something in that hand
        #TODO: gotta figure out two-handed weapons
        """
        return status

    def unwield(self, hand):
        status = 0
        """
        hand = "{}_hand".format(hand)
        if self.eq.get(hand) is not None:
            item = self.eq[hand]
            self.eq[hand] = None
            if hasattr(item, "attack_bonus"): self.remove_attack_bonus(item) if hasattr(item, "armour_bonus"):
                # currently, I'm assuming shield are the only thing you
                #   can wield that will give AC bonus
                self.remove_armour_bonus("shield", item.armour_bonus, item)
        else:
            status = 5      # there's nothing in that hand
        """
        return status
                
    def die(self):
        add_status_effect(self, Afflictions.dead)


