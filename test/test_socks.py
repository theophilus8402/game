#!/usr/bin/python3.4

import unittest
import sys
import control.socks

class socks_login(unittest.TestCase):

    def setUp(self):
        self.world = control.socks.World()
        self.world.passwds["bob"] = "bob123"
        self.bob = control.socks.LoginGuy()
        self.bob.sock = sys.stdout

    def test_socks_login_get_name(self):
        control.socks.login(self.world, self.bob)
        self.assertEqual(self.world.outputs, [self.bob.sock])
        next_msg = self.bob.msg_queue.get_nowait()
        self.assertEqual(next_msg, b"What is your name? \n")
        self.assertEqual(self.bob.name, None)
        self.assertEqual(self.bob.special_state, True)
        self.assertEqual(self.bob.state, "login")

    def test_socks_login_get_name_outputs_not_empty(self):
        control.socks.login(self.world, self.bob)
        self.assertNotEqual(self.world.outputs, [])

    def test_socks_login_recv_name(self):
        control.socks.login(self.world, self.bob, "bob")
        next_msg = self.bob.msg_queue.get_nowait()
        self.assertEqual(next_msg, b"Ah, so your name is bob?\n")
        next_msg = self.bob.msg_queue.get_nowait()
        self.assertEqual(next_msg, b"Please enter your password: \n")
        self.assertEqual(self.bob.name, "bob")
        self.assertEqual(self.bob.special_state, True)
        self.assertEqual(self.bob.state, "login")

    def test_socks_login_recv_pass(self):
        self.bob.name = "bob"
        control.socks.login(self.world, self.bob, "bob123")
        next_msg = self.bob.msg_queue.get_nowait()
        self.assertEqual(next_msg, b"Hey! Your password is correct!\n")
        self.assertEqual(self.bob.name, "bob")
        self.assertEqual(self.bob.special_state, False)
        self.assertEqual(self.bob.state, None)

    def test_socks_login_bad_name(self):
        control.socks.login(self.world, self.bob, "job")
        next_msg = self.bob.msg_queue.get_nowait()
        self.assertEqual(next_msg, b"Ah, so your name is job?\n")
        next_msg = self.bob.msg_queue.get_nowait()
        self.assertEqual(next_msg,
            b"Sorry! You don't exist! Gimme a new name: \n")
        self.assertEqual(self.bob.name, None)
        self.assertEqual(self.bob.special_state, True)
        self.assertEqual(self.bob.state, "login")

    def test_socks_login_bad_pass(self):
        self.bob.name = "bob"
        control.socks.login(self.world, self.bob, "bob1234")
        next_msg = self.bob.msg_queue.get_nowait()
        self.assertEqual(next_msg, b"Sorry! Wrong password!\n")
        self.assertEqual(self.bob.special_state, True)
        self.assertEqual(self.bob.state, "login")

if __name__ == '__main__':
    unittest.main()
