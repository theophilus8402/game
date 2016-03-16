#!/usr/bin/python3.4

from copy import copy
import unittest
import sys

from model.info import Status
from model.tile import *
from model.world import *
import play

class tile(unittest.TestCase):

    def setUp(self):
        self.tile = Tile()

        self.world = play.make_world()

        self.bob = play.make_bob()
        self.bob_tile = get_tile(self.world, Coord(1, 2))
        add_entity(self.bob_tile, self.bob)

        self.sword = play.make_sword()
        self.sword_tile = get_tile(self.world, Coord(1, 3))
        add_entity(self.sword_tile, self.sword)

        self.tim = play.make_tim()
        self.tim_tile = get_tile(self.world, Coord(2, 2))
        add_entity(self.tim_tile, self.tim)

        self.dog = play.make_dog()
        self.dog_tile = get_tile(self.world, Coord(-1, 2))
        add_entity(self.dog_tile, self.dog)

        self.empty_tile = get_tile(self.world, Coord(0, 0))

    def test_addremove_entity(self):
        add_entity(self.tile, self.bob)
        self.assertEqual(self.tile.entities, [self.bob])

        add_entity(self.tile, self.sword)
        self.assertEqual(self.tile.entities, [self.bob, self.sword])

        remove_entity(self.tile, self.bob)
        self.assertEqual(self.tile.entities, [self.sword])

        self.assertEqual(remove_entity(self.tile, self.sword), 
            Status.all_good)
        self.assertEqual(self.tile.entities, [])

        self.assertEqual(remove_entity(self.tile, self.sword), 
            Status.entity_not_in_tile)

    def test_check_tile_new_entity(self):
        self.assertEqual(self.bob.peeps_nearby, set())

        check_tile_new_entity(self.empty_tile, self.bob)
        self.assertEqual(self.bob.peeps_nearby, set())

        check_tile_new_entity(self.bob_tile, self.bob)
        self.assertEqual(self.bob.peeps_nearby, set())

        check_tile_new_entity(self.tim_tile, self.bob)
        self.assertEqual(self.bob.peeps_nearby, {self.tim})
        self.assertEqual(self.tim.peeps_nearby, {self.bob})

        check_tile_new_entity(self.sword_tile, self.bob)
        self.assertEqual(self.bob.peeps_nearby, {self.tim, self.sword})
        self.assertEqual(self.tim.peeps_nearby, {self.bob})
        self.assertEqual(self.sword.peeps_nearby, {self.bob})
        #self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
