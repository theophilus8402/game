#!/usr/bin/python3.4

from world import World,generate_map,InvalidCoords,CoordsOccupied,set_map,display_map,Transaction

import unittest

class TestWorld(unittest.TestCase):

    def setUp(self):
        self.world = World(game_id=1)

    def test_world_init(self):
        self.assertEqual(self.world.game_id, 1)
        self.assertEqual(self.world.map[(0, 0)], None)

        self.assertEqual(self.world.transaction_actions["set_piece"],
            (self.world.set_piece, self.world.undo_set_piece))

    def test_generate_map(self):
        game_map = generate_map()
        self.assertEqual(game_map[(-1, 1)], None)
        self.assertEqual(game_map[(0, 1)], None)
        self.assertEqual(game_map[(1, 1)], None)
        self.assertEqual(game_map[(-1, 0)], None)
        self.assertEqual(game_map[(0, 0)], None)
        self.assertEqual(game_map[(1, 0)], None)
        self.assertEqual(game_map[(-1, -1)], None)
        self.assertEqual(game_map[(0, -1)], None)
        self.assertEqual(game_map[(1, -1)], None)
        self.assertTrue((2, 1) not in game_map.keys())
        self.assertEqual(len(game_map.keys()), 9)

    def test_world_set_piece(self):
        # test valid coords
        # invalid coords should raise InvalidCoords exception
        try:
            self.world.set_piece("x", (2, 1))
        except InvalidCoords:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        self.world.set_piece("x", (1, 1))

        # make sure placement for already occupied spot raises CoordsOccupied
        try:
            self.world.set_piece("x", (1, 1))
        except CoordsOccupied:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        # test placement of pieces
        self.assertEqual(self.world.map[(1, 1)], "x")

    def test_world_undo_set_piece(self):

        # test valid coords
        # invalid coords should raise InvalidCoords exception
        try:
            self.world.undo_set_piece("x", (2, 1))
        except InvalidCoords:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        # Nothing should start at coords (1, 1)
        coords = (1, 1)
        self.assertEqual(self.world.map[coords], None)

        # put something there to undo it
        self.world.set_piece("x", coords)
        self.assertEqual(self.world.map[coords], "x")

        # undo the set_piece
        self.world.undo_set_piece("x", coords)
        self.assertEqual(self.world.map[coords], None)
 
    def test_world_winner(self):

        # make sure winner is None until there's a winner
        world2 = World(game_id=2)
        self.assertEqual(world2.winner, None)
        world2.set_piece("o", (0, 0))
        self.assertEqual(world2.winner, None)

        # make "x" a horizontal winner
        for x in world2.x_range:
            world2.set_piece("x", (x, 1))
        self.assertEqual(world2.winner, "x")

        # make "o" a vertical winner
        world3 = World(game_id=3)
        world3.set_piece("o", (1, 1))
        self.assertEqual(world3.winner, None)
        world3.set_piece("x", (0, 0))
        self.assertEqual(world3.winner, None)
        world3.set_piece("o", (1, 0))
        world3.set_piece("o", (1, -1))
        self.assertEqual(world3.winner, "o")

        # make "x" a diagonal winner
        world4 = World(game_id=4)
        set_map(world4, ["xoo", "ox.", "oxx"])
        self.assertEqual(world4.winner, "x")

        # make "o" a diagonal winner
        world5 = World(game_id=5)
        set_map(world5, ["oxo", "xox", "oox"])
        self.assertEqual(world5.winner, "o")

    def test_world_game_over(self):

        # make sure game_over once all spots are filled
        world2 = World(game_id=2)
        self.assertEqual(world2.game_over, False)
        for coords in [(-1, 1), (0, 1), (-1, 0), (1, 0), (0, -1)]:
            world2.set_piece("x", coords)
        self.assertEqual(world2.game_over, False)
        for coords in [(1, 1), (0, 0), (-1, -1), (1, -1)]:
            world2.set_piece("o", coords)
        # should be over by now because all spots are filled
        self.assertEqual(world2.game_over, True)

        # make sure game_over when winner is True
        world3 = World(game_id=3)
        self.assertEqual(world3.game_over, False)
        for coords in [(-1, 1), (0, 1), (1, 1)]:
            world3.set_piece("x", coords)
        # x should be the winner, so game_over should be True
        self.assertEqual(world3.game_over, True)

    def test_apply_transaction(self):

        coords = (1, 1)
        trans = {
                    "action" : "set_piece",
                    "input"  : {"piece": "x", "coords": coords},
                }
        #trans = Transaction("set_piece", {"piece": "x", "coords": coords})
        self.world.apply_transaction(trans)

        # make sure "x" is in coords
        self.assertEqual(self.world.map[coords], "x")

    def test_undo_transaction(self):

        coords = (-1, 0)
        trans = {
                    "action" : "set_piece",
                    "input"  : {"piece": "x", "coords": coords},
                    "undo"   : True,
                }
        #trans = Transaction("set_piece", {"piece": "x", "coords": coords})
        self.world.apply_transaction(trans)
        self.assertEqual(self.world.map[coords], "x")

        self.world.undo_transaction(trans)
        self.assertEqual(self.world.map[coords], None)

if __name__ == '__main__':
    unittest.main()

