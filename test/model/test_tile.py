#!/usr/bin/python3.4

import unittest
import sys
import model.tile

class world(unittest.TestCase):

    def setUp(self):
        self.world = model.tile.World()
        self.world.passwds["bob"] = "bob123"
        self.bob = model.entity.Player()
        self.bob.sock = sys.stdout
        self.bob.world = self.world
        self.tile = model.tile.Tile()
        self.bob.cur_loc = (0, 0)
        self.world.tiles[(0, 0)] = self.tile
        self.world.max_ent_uid = 5

    def test_get_new_ent_uid(self):
        self.assertEqual(self.world.get_new_ent_uid(), 6)
        self.assertEqual(self.world.get_new_ent_uid(), 7)
        #self.assertFalse(self.world is None)


if __name__ == '__main__':
    unittest.main()
