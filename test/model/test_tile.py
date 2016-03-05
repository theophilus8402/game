#!/usr/bin/python3.4

import unittest
import sys

from model.info import Status
import model.tile
import model.world
import play

class tile(unittest.TestCase):

    def setUp(self):
        self.world = model.world.World()
        self.world.passwds["bob"] = "bob123"
        self.bob = play.make_bob()
        self.bob.sock = sys.stdout
        self.bob.world = self.world
        self.tile = model.tile.Tile()
        self.world.max_ent_uid = 5

        self.sword = play.make_sword()

    def test_addremove_entity(self):
        model.tile.add_entity(self.tile, self.bob)
        self.assertEqual(self.tile.entities, [self.bob])

        model.tile.add_entity(self.tile, self.sword)
        self.assertEqual(self.tile.entities, [self.bob, self.sword])

        model.tile.remove_entity(self.tile, self.bob)
        self.assertEqual(self.tile.entities, [self.sword])

        self.assertEqual(model.tile.remove_entity(self.tile, self.sword), 
            Status.all_good)
        self.assertEqual(self.tile.entities, [])

        self.assertEqual(model.tile.remove_entity(self.tile, self.sword), 
            Status.entity_not_in_tile)
        #self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
