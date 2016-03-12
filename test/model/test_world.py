#!/usr/bin/python3.4

import unittest
import sys

from model.info import Status
from model.tile import *
import model.world
import play

class world(unittest.TestCase):

    def setUp(self):
        self.world = play.make_world()
        self.world.max_ent_uid = 5

        #self.world.passwds["bob"] = "bob123"
        self.bob = play.make_bob()
        #self.bob.sock = sys.stdout
        self.bob.world = self.world

        self.tim = play.make_bob()
        #self.tim.sock = sys.stdout
        self.tim.world = self.world

        self.tile1 = Tile()
        self.tile1.coord = Coord(0, 0)
        add_entity(self.tile1, self.bob)

        self.tile2 = Tile()
        self.tile2.coord = Coord(0, 1)
        add_entity(self.tile2, self.tim)


    def test_distance_between_entities(self):
        dist = model.world.distance_between_coords(self.bob.coord, self.tim.coord)
        self.assertEqual(dist, 1)

        self.tile3 = Tile()
        self.tile3.coord = Coord(5, 5)
        remove_entity(self.tile2, self.tim)
        add_entity(self.tile3, self.tim)
        dist = model.world.distance_between_coords(self.bob.coord, self.tim.coord)
        self.assertTrue(dist>=5)

        self.tile4 = Tile()
        self.tile4.coord = Coord(-4, 1)
        remove_entity(self.tile3, self.tim)
        add_entity(self.tile4, self.tim)
        dist = model.world.distance_between_coords(self.bob.coord, self.tim.coord)
        self.assertTrue(dist>=4)


    def test_get_tile(self):
        #for tile in self.world.tiles:
        #    print(tile.coord)
        tile = model.world.get_tile(self.world, Coord(0, 1))
        self.assertEqual(tile.coord, Coord(0, 1))

        tile = model.world.get_tile(self.world, Coord(0, 0))
        self.assertEqual(tile.coord, Coord(0, 0))

        tile = model.world.get_tile(self.world, Coord(2, 1))
        self.assertEqual(tile.coord, Coord(2, 1))


if __name__ == '__main__':
    unittest.main()
