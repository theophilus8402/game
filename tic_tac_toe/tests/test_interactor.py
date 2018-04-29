#!/usr/bin/python3.4

from interactor import *
from unique_dict import *

import sys
import unittest

class TestCreateWorld(unittest.TestCase):

    def setUp(self):
        self.interactor = Interactor()

    def test_create_world(self):

        self.assertEqual(self.interactor.worlds, {})

        self.interactor.create_world(0)
        self.assertEqual(self.interactor.worlds[0].game_id, 0)
        self.assertEqual(len(self.interactor.worlds), 1)

        self.interactor.create_world(1)
        self.assertEqual(self.interactor.worlds[1].game_id, 1)
        self.assertEqual(len(self.interactor.worlds), 2)

        # should raise an exception duplicating game_id's
        try:
            self.interactor.create_world(1)
            self.assertTrue(False)
        except WorldKeyError as err:
            self.assertTrue(True)

    def test_undo_create_world(self):

        self.assertEqual(self.interactor.worlds, {})

        self.interactor.create_world(0)
        self.assertEqual(self.interactor.worlds[0].game_id, 0)
        self.assertEqual(len(self.interactor.worlds), 1)

        self.interactor.create_world(1)
        self.assertEqual(self.interactor.worlds[1].game_id, 1)
        self.assertEqual(len(self.interactor.worlds), 2)

        self.interactor.undo_create_world(1)
        self.assertTrue(1 not in self.interactor.worlds.keys())
        self.assertEqual(len(self.interactor.worlds), 1)

        # should raise an exception when game_id doesn't exist
        try:
            self.interactor.undo_create_world(1)
            self.assertTrue(False)
        except WorldKeyError as err:
            self.assertTrue(True)


class TestPlayer(unittest.TestCase):

    def test_unknown_player(self):

        unk = Player()
        self.assertEqual(unk.name, "unknown0")

        unk1 = Player()
        self.assertEqual(unk1.name, "unknown1")

    def test_player(self):

        bob = Player("Bob")
        self.assertEqual(bob.name, "Bob")
        self.assertEqual(bob.connection, None)
        self.assertEqual(bob.piece, None)
        self.assertEqual(bob.world, None)


class TestCreatePlayer(unittest.TestCase):

    def setUp(self):
        self.interactor = Interactor()

    def test_create_player(self):
        self.interactor.create_player("Bob")
        self.assertEqual(set(self.interactor.players.keys()), {"bob"})

        self.interactor.create_player("Tim")
        self.assertEqual(set(self.interactor.players.keys()), {"bob", "tim"})

        # should error on this
        try:
            self.interactor.create_player("Bob")
            self.assertTrue(False)
        except PlayerKeyError:
            self.assertTrue(True)

    def test_undo_create_player(self):
        # create bob
        self.interactor.create_player("Bob")
        self.assertEqual(set(self.interactor.players.keys()), {"bob"})

        # undo bob
        self.interactor.undo_create_player("Bob")
        self.assertEqual(set(self.interactor.players.keys()), set())

        # should error on this
        try:
            self.interactor.undo_create_player("Bob")
            self.assertTrue(False)
        except PlayerKeyError:
            self.assertTrue(True)


class TestChangeConnection(unittest.TestCase):

    def setUp(self):

        self.interactor = Interactor()
        self.interactor.create_player("Bob")
        self.bob = self.interactor.players["bob"]

    def test_change_connection(self):

        # initial status
        self.assertEqual(self.bob.connection, None)
        self.assertEqual(self.interactor.connections, {})

        self.interactor.change_connection("Bob", None, sys.stdin)

        # after change
        self.assertEqual(self.bob.connection, sys.stdin)
        self.assertEqual(self.interactor.connections[sys.stdin], self.bob)

    def test_undo_change_connection(self):
 
        self.interactor.change_connection("Bob", None, sys.stdin)

        # after change
        self.assertEqual(self.bob.connection, sys.stdin)
        self.assertEqual(self.interactor.connections[sys.stdin], self.bob)

        # undo
        self.interactor.undo_change_connection("Bob", None, sys.stdin)

        # after undo
        self.assertEqual(self.bob.connection, None)
        self.assertEqual(self.interactor.connections, {})


class TestApplyTransaction(unittest.TestCase):

    def setUp(self):

        self.interactor = Interactor()

    def test_trans_create_world(self):

        trans = {   "entity" : "server",
                    "action" : "create_world",
                    "input"  : {"game_id" : 7},
                }

        self.interactor.apply_transaction(trans)

        # should have a world with a game_id 7
        self.assertEqual(len(self.interactor.worlds), 1)
        self.assertEqual(self.interactor.worlds[7].game_id, 7)

        self.interactor.apply_transaction(trans, undo=True)

        # should have a world with a game_id 7
        self.assertEqual(len(self.interactor.worlds), 0)
        self.assertEqual(self.interactor.worlds.get(7), None)


    def test_trans_create_player(self):

        trans = {   "entity" : "server",
                    "action" : "create_player",
                    "input"  : {"name" : "Bob"},
                }

        self.interactor.apply_transaction(trans)

        # should have a player with a name of "Bob"
        self.assertEqual(len(self.interactor.players), 1)
        self.assertEqual(self.interactor.players["bob"].name, "Bob")

        self.interactor.apply_transaction(trans, undo=True)

        # should not have player with a name of "Bob"
        self.assertEqual(len(self.interactor.players), 0)
        self.assertEqual(self.interactor.players.get("bob"), None)


class TestJoinWorld(unittest.TestCase):

    def setUp(self):

        self.interactor = Interactor()
        self.interactor.create_player("Bob")
        self.bob = self.interactor.players["bob"]

        self.interactor.create_player("Tim")
        self.tim = self.interactor.players["tim"]

        self.interactor.create_player("Billy")
        self.billy = self.interactor.players["billy"]

        self.interactor.create_world(0)
        self.world = self.interactor.worlds[0]

    def test_join_world(self):

        self.interactor.join_world("bob", 0)

        self.assertEqual(self.bob.piece, "o")
        self.assertEqual(self.bob.world, 0)
        self.assertEqual(self.world.game_id, 0)
        self.assertEqual(self.world.o_player, "Bob")

        try:
            self.interactor.join_world("bob", 0)
            self.assertTrue(False)
        except PlayerAlreadyInWorld:
            self.assertTrue(True)

    def test_undo_join_world(self):

        self.interactor.join_world("bob", 0)

        self.assertEqual(self.bob.piece, "o")
        self.assertEqual(self.bob.world, 0)
        self.assertEqual(self.world.game_id, 0)
        self.assertEqual(self.world.o_player, "Bob")

        self.interactor.undo_join_world("bob", 0)

        self.assertEqual(self.bob.piece, None)
        self.assertEqual(self.bob.world, None)
        self.assertEqual(self.world.game_id, 0)
        self.assertEqual(self.world.o_player, None)

    def test_join_world_full(self):

        self.interactor.join_world("bob", 0)
        self.interactor.join_world("tim", 0)

        self.assertEqual(self.bob.piece, "o")
        self.assertEqual(self.tim.piece, "x")

        try:
            self.interactor.join_world("billy", 0)
            self.assertTrue(False)
        except WorldFull:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()

