#!/usr/bin/python3.4

from interactor import *

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
        except WorldExists as err:
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
        except WorldDoesNotExist as err:
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
        except NameExists:
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
        except NameDoesNotExist:
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


if __name__ == '__main__':
    unittest.main()

