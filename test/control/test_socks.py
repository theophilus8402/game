#!/usr/bin/python3.4

import unittest
import sys
import control.socks
import model.tile
import model.world
import play

class socks_add_remove_connection(unittest.TestCase):

    def setUp(self):
        self.world = model.world.World()
        self.world.passwds["bob"] = "bob123"
        self.bob = play.make_bob()
        self.bob.sock = sys.stdout
        self.bob.world = self.world
        self.tile = model.tile.Tile()
        self.bob.cur_loc = (0, 0)
        self.world.tiles[(0, 0)] = self.tile

    def test_socks_add_conn(self):
        control.socks.add_connection(self.world, sys.stdout, self.bob)
        self.assertEqual(self.bob.sock, sys.stdout)
        self.assertEqual(self.world.sock_peeps[sys.stdout], self.bob)

    def test_socks_rem_conn(self):
        self.world.living_ents[self.bob.name] = self.bob
        control.socks.add_connection(self.world, sys.stdout, self.bob)
        self.assertFalse(self.world is None)
        control.socks.remove_connection(self.world, sys.stdout)
        self.assertFalse(sys.stdout in self.world.sock_peeps.keys())
        self.assertFalse(sys.stdout in self.world.outputs)


class socks_send_msg(unittest.TestCase):

    def setUp(self):
        self.world = model.world.World()
        self.world.passwds["bob"] = "bob123"
        self.bob = play.make_bob()
        self.bob.sock = sys.stdout
        self.bob.world = self.world

    """
    def test_socks_send_msg_b(self):
        control.socks.send_msg(self.world, self.bob, b'hello')
        msg = self.bob.msg_queue.get_nowait()
        self.assertEqual(msg, b"hello\n")
    """

    def test_socks_send_msg_s(self):
        self.bob.send_msg("hello")
        msg = self.bob.msg_queue.get_nowait()
        self.assertEqual(msg, b"hello\n")


class socks_login(unittest.TestCase):

    def setUp(self):
        self.world = model.world.World()
        self.world.passwds["bob"] = "bob123"
        self.bob = play.make_bob()
        self.bob.sock = sys.stdout
        self.bob.world = self.world
        self.living_bob = model.entity.Living()
        self.living_bob.name = "bob"
        self.world.living_ents[self.living_bob.name] = self.living_bob
        self.tile = model.tile.Tile()
        self.bob.cur_loc = (0, 0)
        self.world.tiles[(0, 0)] = self.tile

    def test_socks_login_get_name(self):
        control.socks.login(self.world, self.bob)
        self.assertEqual(self.world.outputs, [self.bob.sock])
        #next_msg = self.bob.msg_queue.get_nowait()
        #self.assertEqual(next_msg, b"What is your name? \n")
        self.assertEqual(self.bob.name, None)
        self.assertEqual(self.bob.special_state, "login")

    def test_socks_login_get_name_outputs_not_empty(self):
        control.socks.login(self.world, self.bob)
        self.assertNotEqual(self.world.outputs, [])

    def test_socks_login_recv_name(self):
        control.socks.login(self.world, self.bob, "bob")
        #next_msg = self.bob.msg_queue.get_nowait()
        #self.assertEqual(next_msg, b"Ah, so your name is bob?\n")
        #next_msg = self.bob.msg_queue.get_nowait()
        #self.assertEqual(next_msg, b"Please enter your password: \n")
        self.assertEqual(self.bob.name, "bob")
        self.assertEqual(self.bob.special_state, "login")

    def test_socks_login_recv_pass(self):
        self.bob.name = "bob"
        self.bob.special_state = "login"
        control.socks.login(self.world, self.bob, "bob123")
        next_msg = self.bob.msg_queue.get_nowait()
        self.assertEqual(next_msg, b"Hey! Your password is correct!\n")
        self.assertEqual(self.bob.name, "bob")
        self.assertEqual(self.bob.special_state, None)

    def test_socks_login_bad_name(self):
        control.socks.login(self.world, self.bob, "job")
        next_msg = self.bob.msg_queue.get_nowait()
        self.assertEqual(next_msg, b"Ah, so your name is job?\n")
        next_msg = self.bob.msg_queue.get_nowait()
        self.assertEqual(next_msg,
            b"Sorry! You don't exist! Gimme a new name: \n")
        self.assertEqual(self.bob.name, None)
        self.assertEqual(self.bob.special_state, "login")

    def test_socks_login_bad_pass(self):
        self.bob.name = "bob"
        control.socks.login(self.world, self.bob, "bob1234")
        next_msg = self.bob.msg_queue.get_nowait()
        self.assertEqual(next_msg, b"Sorry! Wrong password!\n")
        self.assertEqual(self.bob.special_state, "login")

    def test_socks_login_no_login(self):
        # testing the function call when we shouldn't be here
        self.bob.name = "bob"
        self.bob.special_state = False
        self.bob.state = None
        control.socks.login(self.world, self.bob)

if __name__ == '__main__':
    unittest.main()
