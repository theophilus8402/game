#!/usr/bin/python3

from collections import defaultdict
import enum

from model.info import Status
from model.entity.inventory import *
from model.special_effect import Effect
from model.util import RollType

@enum.unique
class EqSlots(enum.Enum):
    head = 1
    right_hand = 2
    left_hand = 3
    torso = 4
    leggings = 5
    right_leg = 6
    left_leg = 7
    right_ring_finger = 8
    left_ring_finger = 9
    necklace = 10
    tunic = 11
    ring_finger = 12
    hand = 13


eq_slot_names = {
    EqSlots.head : "head",
    EqSlots.right_hand : "right hand",
    EqSlots.left_hand : "left hand",
    EqSlots.torso : "torso",
    EqSlots.leggings : "legs",
    EqSlots.right_leg : "right_leg",
    EqSlots.left_leg : "left_leg",
    EqSlots.right_ring_finger : "right ring finger",
    EqSlots.left_ring_finger : "left ring finger",
    EqSlots.necklace : "around {actor_poss} neck",
    EqSlots.tunic : "chest",
    }


class BaseEquipment():

    allowed_eq_slots = set()

    def __init__(self):
        self.possibilities = defaultdict(lambda: 0)
        self.special_effects = set()
        self._equipment = defaultdict(lambda: None)# keys: eqslot, value: eq
        # keep a list of all bonuses/penalties due to spells/skills/items...
        self.bonuses = {slot : [] for slot in self.allowed_eq_slots}

    def __len__(self):
        return len(self._equipment)

    def __getitem__(self, eqslot):
        return self._equipment.get(eqslot)

    def items(self):
        return self._equipment.items()

    def __contains__(self, item):
        """
        Returns True if item amongst the equipment.
        Returns False if item not in equipment.
        """
        return item in self._equipment.values()

    def __setitem__(self, key, value):
        if key in self.allowed_eq_slots and self._equipment[key] is None:
            self._equipment[key] = value

    def __delitem__(self, key):
        del(self._equipment[key])

    def add_bonus(self, item, bonus):
        self.item.add_bonus(bonus)


class HumanoidEquipment(BaseEquipment):

    allowed_eq_slots = {
            EqSlots.head,
            EqSlots.right_hand,
            EqSlots.left_hand,
            EqSlots.torso,
            EqSlots.leggings,
            EqSlots.right_leg,
            EqSlots.left_leg,
            EqSlots.right_ring_finger,
            EqSlots.left_ring_finger,
            EqSlots.necklace,
            EqSlots.tunic,
        }
 
    def __init__(self):
        super().__init__()
        self.main_hand_bonuses = EqSlotBonuses()
        self.off_hand_bonuses = EqSlotBonuses()

    def add_bonus(self, item, bonus):
        super().add_bonus(item, bonus)
        # find out if the item should update hand bonuses
        for eq_slot, eq_item in self._equipment.items():
            if eq_item == item:
                if eq_slot == EqSlots.right_hand:
                    self.main_hand_bonuses.add_bonus(bonus)
                elif eq_slot == EqSlots.left_hand:
                    self.off_hand_bonuses.add_bonus(bonus)


class EqSlotBonuses():

    def __init__(self):
        self.bonuses = []
        self.attack_bonus = 0
        self.dmg_bonus = 0

    def add_bonus(self, bonus):
        # NOTE: ability bonuses will have to come in the form of
        #   attack and/or dmg bonuses, not as normal AbilityBonuses
        #   because attack bonus could be dex and dmg bonus could be str
        self.bonuses.append(bonus)
        self.calculate_total()

    def calculate_total(self):
        self.attack_bonus = 0
        self.dmg_bonus = 0
        for bonus in self.bonuses:
            if isinstance(bonus, AttackBonus):
                self.attack_bonus += bonus.amount
            elif isinstance(bonus, DmgBonus):
                self.dmg_bonus += bonus.amount


def get_eq_slot_name(eq_slot):
    return eq_slot_names[eq_slot]


possible_equipment_slots = [
        EqSlots.head,
        EqSlots.right_hand,
        EqSlots.left_hand,
        EqSlots.torso,
        EqSlots.leggings,
        EqSlots.right_leg,
        EqSlots.left_leg,
        EqSlots.right_ring_finger,
        EqSlots.left_ring_finger,
        EqSlots.necklace,
        EqSlots.tunic,
        ]


def check_slots_open(eq, slots):
    """
    Given a list of equipment slots to try, will return the first open equipment
    slot.  If not equipment slot is available, False will be returned.
    """
    for slot in slots:
        if eq[slot] == None:
            return slot
    return None


def determine_eq_slot(entity, item, side=None):
    """
    Returns which (if any) slot should be use to equip the item.  Will take into
    strong consideration if a side is provided by the entity.  If no side is provided
    and one must be chosen, the right side will be perferred, but left may be used
    if the right side is already filled.  If there is no appropriate slot available,
    False is returned.
    """
    item_eq_slot = item.eq_slot
    eq = entity.equipment
    if item_eq_slot == EqSlots.hand:
        if side == "right":
            options = [EqSlots.right_hand]
        elif side == "left":
            options = [EqSlots.left_hand]
        else:
            options = [EqSlots.right_hand, EqSlots.left_hand]
    elif item_eq_slot == EqSlots.ring_finger:
        if side == "right":
            options = [EqSlots.right_ring_finger]
        elif side == "left":
            options = [EqSlots.left_ring_finger]
        else:
            [EqSlots.right_ring_finger, EqSlots.left_ring_finger]
    else:
        options = [item_eq_slot]
    eq_slot = check_slots_open(eq, options)
    return eq_slot


def entity_can_equip(entity, item, eq_slot):
    """
    Returns Status.all_good if entity can equip the item.
    Else, Status.improper_eq_slot if given an improper eq_slot.
    Else, Status.item_not_in_inventory, or Status.equipment_slot_not_free.
    """

    status = Status.all_good
    eq = entity.equipment

    if not isinstance(eq_slot, EqSlots):
        return Status.improper_eq_slot

    # make sure the item is in the inventory
    if item not in entity.inventory.items.values():
        return Status.item_not_in_inventory

    # make sure the slot is empty
    if check_slots_open(eq, [eq_slot]) != eq_slot:
        return Status.equipment_slot_not_free

    # make sure requirements are met
    # TODO

    return status


def entity_equip_item(entity, item, eq_slot):
    """
    Ensures the entity can equip the item in the given eq_slot.
    Removes the item from the inventory.
    Equips the item.
    Adds any bonuses/detriments.
    """
    status = Status.all_good
    eq = entity.equipment
    inv = entity.inventory

    # make sure entity can equip it
    status = entity_can_equip(entity, item, eq_slot)
    if status != Status.all_good:
        return status

    # remove the item from the inventory
    status = inventory_remove_item(inv, item)
    if status != Status.all_good:
        return status

    # equip the item
    eq[eq_slot] = item

    # add any benefits/detriments provided by the item
    # TODO

    return status


def equipment_has_item(eq, item):
    """Returns the eq_slot in which the item resides, else returns None."""
    eq_slot = None
    for temp_eq_slot, temp_item in eq.items():
        if temp_item == item:
            eq_slot = temp_eq_slot
            break
    return eq_slot


def entity_remove_item(entity, item):
    """
    Makes sure the item is in the entity's equpment (Status.item_not_in_equipment).
    Makes sure the inventory can fit the item.
    Removes any benefits/detriments provided by the item.
    Removes the item from the equipment.    
    Adds the item to the inventory.
    """

    eq = entity.equipment
    inv = entity.inventory

    # make sure the item is among the equipment being worn
    eq_slot = equipment_has_item(eq, item)
    if not eq_slot:
        return Status.item_not_in_equipment

    # make sure the item can fit in the inventory
    status = inventory_can_add_item(inv, item)
    if status != Status.all_good:
        return status

    # remove any benefits/detriments provided by the item
    # TODO

    # remove the item from the equipment slot
    eq[eq_slot] = None
    
    # add the item to the inventory
    status = inventory_add_item(inv, item)

    return status


