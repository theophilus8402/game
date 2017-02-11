#!/usr/bin/python3.4

import unittest

from model.entity.inventory import *
import play

class TestInventory(unittest.TestCase):

    def setUp(self):

        self.inv = Inventory(volume_capacity=10, weight_capacity=30)

        # Bob's vol=12, weight=192
        # sword's vol=1, weight=6
        # shield's vol=3, weight=5
        # bow's vol=1, weight=6
        # shoe's vol=.5, weight=1
        # armour's vol=6, weight=19
        # dog's vol=4, weight=41
        self.bob = play.make_bob()
        self.sword = play.make_sword()
        self.shield = play.make_shield()
        self.bow = play.make_bow()
        self.shoes = play.make_shoes()
        self.armour = play.make_armour()
        self.dog = play.make_dog()

    def test_inventory_get_items(self):
        self.inv.items = {"sword": self.sword, "shield": self.shield, "bow": self.bow}
        self.assertEqual(inventory_get_items(self.inv),
            {self.sword, self.shield, self.bow})

    def test_inventory_get_current_capacity(self):
        self.inv.current_items_volume = 19
        self.inv.current_items_weight = 32
        self.assertEqual(inventory_get_current_capacity(self.inv), (19, 32))

    def test_inventory_add_item(self):
        inventory_add_item(self.inv, self.sword)
        self.assertEqual(inventory_get_items(self.inv), {self.sword})
        self.assertEqual(inventory_get_current_capacity(self.inv), (1, 6))

        inventory_add_item(self.inv, self.bow)
        self.assertEqual(inventory_get_items(self.inv),
            {self.sword, self.bow})
        self.assertEqual(inventory_get_current_capacity(self.inv), (2, 12))

    def test_inventory_can_add_item(self):
        for item in [self.sword, self.shield, self.bow, self.shoes]:
            self.assertEqual(inventory_can_add_item(self.inv, item), Status.all_good)
            inventory_add_item(self.inv, item)
        # should be at vol=5.5 and weight=18
        self.assertEqual(inventory_get_current_capacity(self.inv), (5.5, 18))

        self.assertEqual(inventory_can_add_item(self.inv, self.dog),
            Status.item_too_heavy)

        self.assertEqual(inventory_can_add_item(self.inv, self.armour),
            Status.item_too_big)

    def test_inventory_find_item(self):
        self.assertEqual(inventory_find_item(self.inv, "short sword"), None)

        for item in [self.sword, self.shield, self.bow, self.shoes]:
            inventory_add_item(self.inv, item)

        self.assertEqual(inventory_find_item(self.inv, "short sword"), self.sword)
        self.assertEqual(inventory_find_item(self.inv, "sword"), None)
        self.assertEqual(inventory_find_item(self.inv, "short bow"), self.bow)

    def test_inventory_remove_item(self):

        self.assertEqual(inventory_remove_item(self.inv, self.bow),
            Status.item_not_in_inventory)

        for item in [self.sword, self.shield, self.bow, self.shoes]:
            inventory_add_item(self.inv, item)

        self.assertEqual(inventory_get_items(self.inv),
            {self.sword, self.shield, self.bow, self.shoes})
        # should be at vol=5.5 and weight=18
        self.assertEqual(inventory_get_current_capacity(self.inv), (5.5, 18))

        self.assertEqual(inventory_remove_item(self.inv, self.bow), Status.all_good)
        # should be at vol=4.5 and weight=12
        self.assertEqual(inventory_get_current_capacity(self.inv), (4.5, 12))
        self.assertEqual(inventory_remove_item(self.inv, self.bow),
            Status.item_not_in_inventory)

        self.assertEqual(inventory_remove_item(self.inv, self.sword), Status.all_good)
        # should be at vol=3.5 and weight=6
        self.assertEqual(inventory_get_current_capacity(self.inv), (3.5, 6))
        self.assertEqual(inventory_get_items(self.inv), {self.shield, self.shoes})

        self.assertEqual(inventory_remove_item(self.inv, self.shield), Status.all_good)
        self.assertEqual(inventory_remove_item(self.inv, self.shoes), Status.all_good)
        # should be at vol=0 and weight=0
        self.assertEqual(inventory_get_current_capacity(self.inv), (0.0, 0))
        self.assertEqual(inventory_get_items(self.inv), set())

