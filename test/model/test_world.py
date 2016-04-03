#!/usr/bin/python3.4

import unittest
import sys

from model.info import Status
from model.tile import *
from model.world import *
import play

class world(unittest.TestCase):

    def setUp(self):
        self.world = play.make_world()
        self.world.max_ent_uid = 5

        self.bob = play.make_bob()
        self.bob_tile = get_tile(self.world, Coord(1, 2))

        self.sword = play.make_sword()
        self.sword_tile = get_tile(self.world, Coord(1, 3))

        self.tim = play.make_tim()
        self.tim_tile = get_tile(self.world, Coord(2, 2))

        self.dog = play.make_dog()
        self.dog_tile = get_tile(self.world, Coord(-1, 2))

        self.armour = play.make_armour()
        self.armour_tile = get_tile(self.world, Coord(3, -4))

        self.empty_tile = get_tile(self.world, Coord(0, 0))


        self.tile1 = Tile()
        self.tile1.coord = Coord(0, 0)
        self.tile2 = Tile()
        self.tile2.coord = Coord(0, 1)
        self.tile3 = Tile()
        self.tile3.coord = Coord(5, 5)
        self.tile4 = Tile()
        self.tile4.coord = Coord(-4, 1)
 

    def test_distance_between_entities(self):
        add_entity(self.tile1, self.bob)
        add_entity(self.tile2, self.tim)

        dist = distance_between_coords(self.bob.coord, self.tim.coord)
        self.assertEqual(dist, 1)

        remove_entity(self.tile2, self.tim)
        add_entity(self.tile3, self.tim)
        dist = distance_between_coords(self.bob.coord, self.tim.coord)
        self.assertTrue(dist>=5)

        remove_entity(self.tile3, self.tim)
        add_entity(self.tile4, self.tim)
        dist = distance_between_coords(self.bob.coord, self.tim.coord)
        self.assertTrue(dist>=4)

    def test_get_tile(self):
        tile = get_tile(self.world, Coord(0, 1))
        self.assertEqual(tile.coord, Coord(0, 1))

        tile = get_tile(self.world, Coord(0, 0))
        self.assertEqual(tile.coord, Coord(0, 0))

        tile = get_tile(self.world, Coord(2, 1))
        self.assertEqual(tile.coord, Coord(2, 1))

    def test_check_entities_out_of_range(self):
        add_entity(self.bob_tile, self.bob)
        add_entity(self.sword_tile, self.sword)
        add_entity(self.tim_tile, self.tim)
        add_entity(self.dog_tile, self.dog)

        self.assertEqual(self.bob.peeps_nearby, set())

        check_entities_out_of_range(self.bob, 0, 0)
        self.assertEqual(self.bob.peeps_nearby, set())

        check_tile_new_entity(self.tim_tile, self.bob)
        check_tile_new_entity(self.dog_tile, self.bob)

        check_entities_out_of_range(self.bob, 0, 0)
        self.assertEqual(self.bob.peeps_nearby, {self.tim, self.dog})

        check_entities_out_of_range(self.bob, -1, None)
        self.assertEqual(self.bob.peeps_nearby, {self.tim})
        
        check_tile_new_entity(self.sword_tile, self.bob)
        check_entities_out_of_range(self.bob, 2, 2)
        self.assertEqual(self.bob.peeps_nearby, {self.sword})

        check_entities_out_of_range(self.bob, None, 3)
        self.assertEqual(self.bob.peeps_nearby, set())

    def pseudo_move(self, entity, coord_delta):
        dst_coord = entity.coord + coord_delta
        dst_tile = get_tile(self.world, dst_coord)
        old_tile = get_tile(self.world, entity.coord)
        if dst_tile:
            add_entity(dst_tile, entity)
            remove_entity(old_tile, entity)
            move_check_nearby_entities(self.world, entity, coord_delta)
        else:
            print("Egads! {} doesn't exist!".format(dst_coord))

    def test_move_check_nearby_entities(self):
        self.assertEqual(self.bob.peeps_nearby, set())

        new_bob_tile = get_tile(self.world, Coord(-4, -2))
        remove_entity(self.bob_tile, self.bob)
        add_entity(new_bob_tile, self.bob)
        add_entity(self.sword_tile, self.sword)
        add_entity(self.dog_tile, self.dog)
        add_entity(self.tim_tile, self.tim)
        add_entity(self.armour_tile, self.armour)

        # 432101234
        # ......... 4
        # .....s... 3
        # ...d..t.. 2
        # ......... 1
        # ......... 0
        # .........-1
        # B........-2
        # .........-3
        # .......a.-4

        self.bob.visual_range = 3

        self.pseudo_move(self.bob, Coord(0, 1))
        self.assertEqual(self.bob.peeps_nearby, {self.dog})

        self.pseudo_move(self.bob, Coord(1, 0))
        self.assertEqual(self.bob.peeps_nearby, {self.dog})

        self.pseudo_move(self.bob, Coord(1, 1))
        self.assertEqual(self.bob.peeps_nearby, {self.dog, self.sword})

        self.pseudo_move(self.bob, Coord(1, 0))
        self.assertEqual(self.bob.peeps_nearby, {self.dog, self.sword, self.tim})

        self.pseudo_move(self.bob, Coord(0, -1))
        self.assertEqual(self.bob.peeps_nearby, {self.dog, self.tim})

        self.pseudo_move(self.bob, Coord(1, 0))
        self.assertEqual(self.bob.peeps_nearby, {self.dog, self.tim, self.armour})

    def pseudo_teleport(self, entity, coord):
        old_entity_tile = get_tile(self.world, entity.coord)
        remove_entity(old_entity_tile, entity)
        new_entity_tile = get_tile(self.world, coord)
        add_entity(new_entity_tile, entity)
        area_entity_check(self.world, entity)

    def test_move_entity(self):

        self.assertEqual(self.bob.peeps_nearby, set())

        # 432101234
        # ......... 4
        # .....s... 3
        # ...d..t.. 2
        # ......... 1
        # ......... 0
        # .........-1
        # B........-2
        # .........-3
        # .......a.-4
        add_entity(self.dog_tile, self.dog)
        add_entity(self.sword_tile, self.sword)
        add_entity(self.tim_tile, self.tim)
        add_entity(self.armour_tile, self.armour)
        tmp_bob_tile = get_tile(self.world, Coord(-4, -2))
        add_entity(tmp_bob_tile, self.bob)
        self.bob.visual_range = 3
        self.dog.visual_range = 3
        self.sword.visual_range = 3
        self.tim.visual_range = 3
        self.armour.visual_range = 3

        # do initial checks for entities nearby
        area_entity_check(self.world, self.bob)
        area_entity_check(self.world, self.sword)
        area_entity_check(self.world, self.dog)
        area_entity_check(self.world, self.tim)
        area_entity_check(self.world, self.armour)

        # bob shouldn't see anyone where he starts out
        self.assertEqual(self.bob.peeps_nearby, set())
        self.assertEqual(self.dog.peeps_nearby, {self.sword, self.tim})
        self.assertEqual(self.sword.peeps_nearby, {self.dog, self.tim})
        self.assertEqual(self.tim.peeps_nearby, {self.dog, self.sword})
        self.assertEqual(self.armour.peeps_nearby, set())

        # bob moves right in between the dog, sword, and tim
        move_entity(self.world, self.bob, Coord(1, 2))
        self.assertEqual(self.bob.peeps_nearby, {self.dog, self.sword, self.tim})
        self.assertEqual(self.dog.peeps_nearby, {self.bob, self.sword, self.tim})
        self.assertEqual(self.sword.peeps_nearby, {self.dog, self.bob, self.tim})
        self.assertEqual(self.tim.peeps_nearby, {self.dog, self.sword, self.bob})
        self.assertEqual(self.armour.peeps_nearby, set())

        # walks south a bit
        move_entity(self.world, self.bob, Coord(1, 1))
        self.assertEqual(self.bob.peeps_nearby, {self.dog, self.sword, self.tim})
        move_entity(self.world, self.bob, Coord(1, 0))
        self.assertEqual(self.bob.peeps_nearby, {self.dog, self.sword, self.tim})
        move_entity(self.world, self.bob, Coord(1, -1))
        self.assertEqual(self.bob.peeps_nearby, {self.dog, self.armour, self.tim})
        move_entity(self.world, self.bob, Coord(1, -2))
        self.assertEqual(self.bob.peeps_nearby, {self.armour})

        # walks to the west
        move_entity(self.world, self.bob, Coord(0, -2))
        self.assertEqual(self.bob.peeps_nearby, {self.armour})
        move_entity(self.world, self.bob, Coord(-1, -2))
        self.assertEqual(self.bob.peeps_nearby, set())
        move_entity(self.world, self.bob, Coord(-2, -2))
        self.assertEqual(self.bob.peeps_nearby, set())

        # walks north east
        move_entity(self.world, self.bob, Coord(-1, -1))
        self.assertEqual(self.bob.peeps_nearby, {self.dog, self.tim})

    def test_area_entity_check(self):

        self.assertEqual(self.bob.peeps_nearby, set())

        # 432101234
        # ......... 4
        # .....s... 3
        # ...d..t.. 2
        # ......... 1
        # ......... 0
        # .........-1
        # B........-2
        # .........-3
        # .......a.-4
        add_entity(self.dog_tile, self.dog)
        add_entity(self.sword_tile, self.sword)
        add_entity(self.tim_tile, self.tim)
        add_entity(self.armour_tile, self.armour)
        tmp_bob_tile = get_tile(self.world, Coord(-4, -2))
        add_entity(tmp_bob_tile, self.bob)
        self.bob.visual_range = 3

        # bob shouldn't see anyone while at Coord(-4, -2) w/ visual_range 3
        area_entity_check(self.world, self.bob)
        self.assertEqual(self.bob.peeps_nearby, set())

        # teleport bob to Coord(0, 1) and he should see: dog, sword, tim
        self.pseudo_teleport(self.bob, Coord(0, 1))
        self.assertEqual(self.bob.peeps_nearby, {self.dog, self.sword, self.tim})

        # teleport bob to Coord(4, -3) and he should see: armour
        self.pseudo_teleport(self.bob, Coord(4, -3))
        self.assertEqual(self.bob.peeps_nearby, {self.armour})

        # teleport bob to Coord(-4, -3) and he should see: armour
        self.pseudo_teleport(self.bob, Coord(-4, -3))
        self.assertEqual(self.bob.peeps_nearby, set())


if __name__ == '__main__':
    unittest.main()
