#!/usr/bin/python3.4

import unittest
import sys

from control.comm import *
from model.entity.status_effects import *
from view.msgs import *
from view.info import ViewStatus
import play

class Format_Action_Say_Msg(unittest.TestCase):

    def setUp(self):
        self.bob = play.make_bob()
        self.bob.comms = AI_IO(ai_name=self.bob.name, from_server_file="test_bob.txt")

        self.tim = play.make_tim()
        self.tim.comms = AI_IO(ai_name=self.tim.name, from_server_file="test_tim.txt")

        self.alice = play.make_alice()
        self.alice.comms = AI_IO(ai_name=self.alice.name,
            from_server_file="test_alice.txt")

    def test_num_recips(self):
        msg_info = {}
        #msg_info["say_to"] = True
        msg_info["actor"] = self.bob
        msg_info["recipients"] = []
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob]
        self.assertEqual(format_action_say_msg(msg_info), [(self.bob,
            "You say, 'Hey!'")])

        msg_info = {}
        msg_info["say_to"] = True
        msg_info["actor"] = self.bob
        msg_info["recipients"] = []
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob]
        self.assertEqual(format_action_say_msg(msg_info), View_Status.missing_msg_info)

        msg_info = {}
        #msg_info["say_to"] = True
        msg_info["actor"] = self.bob
        msg_info["recipients"] = [self.bob, self.bob]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob]
        self.assertEqual(format_action_say_msg(msg_info),
            View_Status.too_many_recipients)

        msg_info = {}
        msg_info["say_to"] = True
        msg_info["actor"] = self.bob
        msg_info["recipients"] = [self.bob]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob]
        self.assertEqual(format_action_say_msg(msg_info), [(self.bob,
            "You say to yourself, 'Hey!'")])

        msg_info = {}
        msg_info["say_to"] = True
        msg_info["actor"] = self.bob
        msg_info["recipients"] = [self.bob, self.bob]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob]
        self.assertEqual(format_action_say_msg(msg_info),
            View_Status.too_many_recipients)

    def test_multiple_entities(self):
        msg_info = {}
        #msg_info["say_to"] = True
        msg_info["actor"] = self.bob
        msg_info["recipients"] = []
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_action_say_msg(msg_info), [
            (self.bob, "You say, 'Hey!'"),
            (self.tim, "bob says, 'Hey!'"),
            (self.alice, "bob says, 'Hey!'"),
            ])

        msg_info = {}
        msg_info["say_to"] = False
        msg_info["actor"] = self.bob
        msg_info["recipients"] = [self.tim]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_action_say_msg(msg_info), [
            (self.bob, "You say, 'Hey!'"),
            (self.tim, "bob says, 'Hey!'"),
            (self.alice, "bob says, 'Hey!'"),
            ])

        msg_info = {}
        msg_info["say_to"] = True
        msg_info["actor"] = self.bob
        msg_info["recipients"] = [self.tim]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_action_say_msg(msg_info), [
            (self.bob, "You say to tim, 'Hey!'"),
            (self.tim, "bob says to you, 'Hey!'"),
            (self.alice, "bob says to tim, 'Hey!'"),
            ])

    def test_gender(self):
        msg_info = {}
        msg_info["say_to"] = True
        msg_info["actor"] = self.bob
        msg_info["recipients"] = [self.bob]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_action_say_msg(msg_info), [
            (self.bob, "You say to yourself, 'Hey!'"),
            (self.tim, "bob says to himself, 'Hey!'"),
            (self.alice, "bob says to himself, 'Hey!'"),
            ])

        msg_info = {}
        msg_info["say_to"] = True
        msg_info["actor"] = self.alice
        msg_info["recipients"] = [self.alice]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_action_say_msg(msg_info), [
            (self.bob, "alice says to herself, 'Hey!'"),
            (self.tim, "alice says to herself, 'Hey!'"),
            (self.alice, "You say to yourself, 'Hey!'"),
            ])

    def test_cant_hear(self):
        msg_info = {}
        msg_info["say_to"] = True
        msg_info["actor"] = self.bob
        msg_info["recipients"] = [self.tim]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_action_say_msg(msg_info), [
            (self.bob, "You say to tim, 'Hey!'"),
            (self.tim, "bob says to you, 'Hey!'"),
            (self.alice, "bob says to tim, 'Hey!'"),
            ])

        # Alice shouldn't hear anything
        add_status_effect(self.alice, Afflictions.deaf)
        self.assertEqual(format_action_say_msg(msg_info), [
            (self.bob, "You say to tim, 'Hey!'"),
            (self.tim, "bob says to you, 'Hey!'"),
            (self.alice, "You see bob moving his lips but can't hear anything."),
            ])

    def test_cant_see(self):
        msg_info = {}
        msg_info["say_to"] = True
        msg_info["actor"] = self.bob
        msg_info["recipients"] = [self.tim]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_action_say_msg(msg_info), [
            (self.bob, "You say to tim, 'Hey!'"),
            (self.tim, "bob says to you, 'Hey!'"),
            (self.alice, "bob says to tim, 'Hey!'"),
            ])

        # Alice shouldn't hear anything
        add_status_effect(self.alice, Afflictions.blind)
        self.assertEqual(format_action_say_msg(msg_info), [
            (self.bob, "You say to tim, 'Hey!'"),
            (self.tim, "bob says to you, 'Hey!'"),
            (self.alice, "You hear someone say, 'Hey!'"),
            ])

    def test_blind_and_deaf(self):
        msg_info = {}
        msg_info["say_to"] = True
        msg_info["actor"] = self.bob
        msg_info["recipients"] = [self.tim]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_action_say_msg(msg_info), [
            (self.bob, "You say to tim, 'Hey!'"),
            (self.tim, "bob says to you, 'Hey!'"),
            (self.alice, "bob says to tim, 'Hey!'"),
            ])

        # Alice shouldn't hear anything
        add_status_effect(self.alice, Afflictions.blind)
        add_status_effect(self.alice, Afflictions.deaf)
        self.assertEqual(format_action_say_msg(msg_info), [
            (self.bob, "You say to tim, 'Hey!'"),
            (self.tim, "bob says to you, 'Hey!'"),
            ])

class Format_Msg(unittest.TestCase):

    def setUp(self):
        self.bob = play.make_bob()
        self.bob.comms = AI_IO(ai_name=self.bob.name, from_server_file="test_bob.txt")

        self.tim = play.make_tim()
        self.tim.comms = AI_IO(ai_name=self.tim.name, from_server_file="test_tim.txt")

        self.alice = play.make_alice()
        self.alice.comms = AI_IO(ai_name=self.alice.name,
            from_server_file="test_alice.txt")

    def test_status_msg(self):
        msg_info = {}
        msg_info["msg_type"] = MsgType.action_say
        msg_info["say_to"] = True
        msg_info["actor"] = self.bob
        msg_info["recipients"] = []
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_msg(msg_info), View_Status.missing_msg_info)

    def test_uppercase_msg(self):
        msg_info = {}
        msg_info["msg_type"] = MsgType.action_say
        msg_info["say_to"] = True
        msg_info["actor"] = self.bob
        msg_info["recipients"] = [self.tim]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_msg(msg_info), [
            (self.bob, "You say to tim, 'Hey!'"),
            (self.tim, "Bob says to you, 'Hey!'"),
            (self.alice, "Bob says to tim, 'Hey!'"),
            ])


if __name__ == '__main__':
    unittest.main()
