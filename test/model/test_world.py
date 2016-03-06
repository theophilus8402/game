#!/usr/bin/python3.4

import unittest
import sys

from model.info import Status
import model.tile
import model.world
import play

class world(unittest.TestCase):

    def setUp(self):
        self.world = model.world.World()
        self.world.max_ent_uid = 5

        #self.world.passwds["bob"] = "bob123"
        self.bob = play.make_bob()
        #self.bob.sock = sys.stdout
        self.bob.world = self.world

        self.tim = play.make_bob()
        #self.tim.sock = sys.stdout
        self.tim.world = self.world

        self.tile1 = model.tile.Tile()
        self.tile1.coord = (0, 0)
        model.tile.add_entity(self.tile1, self.bob)

        self.tile2 = model.tile.Tile()
        self.tile2.coord = (0, 1)
        model.tile.add_entity(self.tile2, self.tim)


    def test_distance_between_entities(self):
        dist = model.world.distance_between_entities(self.bob, self.tim)
        self.assertEqual(dist, 1)

        self.tile3 = model.tile.Tile()
        self.tile3.coord = (5, 5)
        model.tile.remove_entity(self.tile2, self.tim)
        model.tile.add_entity(self.tile3, self.tim)
        dist = model.world.distance_between_entities(self.bob, self.tim)
        self.assertTrue(dist>=5)

        self.tile4 = model.tile.Tile()
        self.tile4.coord = (-4, 1)
        model.tile.remove_entity(self.tile3, self.tim)
        model.tile.add_entity(self.tile4, self.tim)
        dist = model.world.distance_between_entities(self.bob, self.tim)
        self.assertTrue(dist>=4)


if __name__ == '__main__':
    unittest.main()
