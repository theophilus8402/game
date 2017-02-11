#!/usr/bin/python3.4

import unittest

from model.entity.living.equip import *
from model.entity.inventory import *
import play

class TestEquip(unittest.TestCase):

    def setUp(self):

        self.eq = {slot: None for slot in possible_equipment_slots}

        self.bob = play.make_bob()
        self.inv = self.bob.inventory
        self.sword = play.make_sword()
        self.shield = play.make_shield()
        self.bow = play.make_bow()
        self.shoes = play.make_shoes()
        self.armour = play.make_armour()
        self.dog = play.make_dog()

        inventory_add_item(self.inv, self.sword)
        inventory_add_item(self.inv, self.shield)
        inventory_add_item(self.inv, self.armour)

    def test_check_slots_open(self):
        self.assertEqual(self.eq[EqSlots.head], None)
        self.assertEqual(self.eq[EqSlots.right_hand], None)
        self.assertEqual(self.eq[EqSlots.left_hand], None)
        self.assertEqual(self.eq[EqSlots.torso], None)
        self.assertEqual(self.eq[EqSlots.leggings], None)
        self.assertEqual(self.eq[EqSlots.feet], None)
        self.assertEqual(self.eq[EqSlots.left_ring_finger], None)

        options = [EqSlots.right_hand, EqSlots.left_hand]
        self.assertEqual(check_slots_open(self.eq, options), EqSlots.right_hand)
        self.eq[EqSlots.right_hand] = self.sword
        self.assertEqual(check_slots_open(self.eq, options), EqSlots.left_hand)

        options = [EqSlots.feet]
        self.assertEqual(check_slots_open(self.eq, options), EqSlots.feet)
        self.eq[EqSlots.feet] = self.shoes
        self.assertEqual(check_slots_open(self.eq, options), None)

        options = [EqSlots.torso]
        self.assertEqual(check_slots_open(self.eq, options), EqSlots.torso)
        self.eq[EqSlots.torso] = self.armour
        self.assertEqual(check_slots_open(self.eq, options), None)

    def test_entity_equip_item(self):
        self.assertEqual(entity_equip_item(self.bob, self.sword, EqSlots.right_hand),
            Status.all_good)
        self.assertEqual(entity_equip_item(self.bob, self.sword, EqSlots.left_hand),
            Status.item_not_in_inventory)
        self.assertEqual(entity_equip_item(self.bob, self.shield, EqSlots.left_hand),
            Status.all_good)
        self.assertEqual(inventory_has_item(self.inv, self.sword), False)
        self.assertEqual(inventory_has_item(self.inv, self.shield), False)

    def test_determine_eq_slot(self):
        slot = determine_eq_slot(self.bob, self.sword)
        self.assertEqual(slot, EqSlots.right_hand)

        slot = determine_eq_slot(self.bob, self.sword, side="left")
        self.assertEqual(slot, EqSlots.left_hand)

        entity_equip_item(self.bob, self.sword, EqSlots.right_hand)
        slot = determine_eq_slot(self.bob, self.sword)
        self.assertEqual(slot, EqSlots.left_hand)

        slot = determine_eq_slot(self.bob, self.sword)
        self.assertEqual(slot, EqSlots.left_hand)

        slot = determine_eq_slot(self.bob, self.shield, side="right")
        self.assertEqual(slot, None)

        slot = determine_eq_slot(self.bob, self.shoes)
        self.assertEqual(slot, EqSlots.feet)

    def test_entity_can_equip(self):
        status = entity_can_equip(self.bob, self.sword, EqSlots.right_hand)
        self.assertEqual(status, Status.all_good)
        entity_equip_item(self.bob, self.sword, EqSlots.right_hand)

        status = entity_can_equip(self.bob, self.sword, EqSlots.right_hand)
        self.assertEqual(status, Status.item_not_in_inventory)

        status = entity_can_equip(self.bob, self.sword, "right_hand")
        self.assertEqual(status, Status.improper_eq_slot)

        status = entity_can_equip(self.bob, self.shield, EqSlots.right_hand)
        self.assertEqual(status, Status.equipment_slot_not_free)


    def test_entity_remove_item(self):
        status = inventory_add_item(self.inv, self.dog)
        self.assertEqual(status, Status.all_good)

        # make sure the item is among the equipment being worn
        status = entity_remove_item(self.bob, self.sword)
        self.assertEqual(status, Status.item_not_in_equipment)

        # make sure the item can fit in the inventory
        status = entity_equip_item(self.bob, self.sword, EqSlots.right_hand)
        self.assertEqual(status, Status.all_good)
        status = entity_equip_item(self.bob, self.shield, EqSlots.left_hand)
        self.assertEqual(status, Status.all_good)
        status = entity_remove_item(self.bob, self.sword)
        self.assertEqual(status, Status.item_too_heavy)

        # remove any benefits/detriments provided by the item
        # TODO

        # remove the item from the equipment slot
        inventory_remove_item(self.inv, self.dog)
        status = entity_remove_item(self.bob, self.sword)
        self.assertEqual(status, Status.all_good)
        slot = EqSlots.right_hand
        self.assertEqual(check_slots_open(self.eq, {slot}), slot)

        # add the item to the inventory
        self.assertEqual(inventory_has_item(self.inv, self.sword), True)

