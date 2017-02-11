#!/usr/bin/python3.4

from collections import defaultdict
import unittest
import sys

from control.comm import *
from model.entity.living.status_effects import *
from view.msgs.basic import *
from view.info import ViewStatus
import play


class FormatActionMsg(unittest.TestCase):

    def setUp(self):
        self.bob = play.make_bob()
        self.bob.comms = AI_IO(ai_name=self.bob.name, from_server_file="test/output/test_bob.txt")

        self.tim = play.make_tim()
        self.tim.comms = AI_IO(ai_name=self.tim.name, from_server_file="test/output/test_tim.txt")

        self.alice = play.make_alice()
        self.alice.comms = AI_IO(ai_name=self.alice.name,
            from_server_file="test/output/test_alice.txt")

    def test_multiple_entities(self):
        msg_info = {}
        msg_info["msg_type"] = MsgType.action_say
        msg_info["actor"] = self.bob
        msg_info["recipients"] = []
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_action_msg(msg_info), [
            (self.bob, "You say, 'Hey!'"),
            (self.tim, "Bob says, 'Hey!'"),
            (self.alice, "Bob says, 'Hey!'"),
            ])

        msg_info = {}
        msg_info["msg_type"] = MsgType.action_say
        msg_info["actor"] = self.bob
        msg_info["recipients"] = []
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_action_msg(msg_info), [
            (self.bob, "You say, 'Hey!'"),
            (self.tim, "Bob says, 'Hey!'"),
            (self.alice, "Bob says, 'Hey!'"),
            ])

        msg_info = {}
        msg_info["msg_type"] = MsgType.action_say_to
        msg_info["actor"] = self.bob
        msg_info["recipients"] = [self.tim]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_action_msg(msg_info), [
            (self.bob, "You say to Tim, 'Hey!'"),
            (self.tim, "Bob says to you, 'Hey!'"),
            (self.alice, "Bob says to Tim, 'Hey!'"),
            ])

    def test_gender(self):
        msg_info = {}
        msg_info["msg_type"] = MsgType.action_say_to
        msg_info["actor"] = self.bob
        msg_info["recipients"] = [self.bob]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_action_msg(msg_info), [
            (self.bob, "You say to yourself, 'Hey!'"),
            (self.tim, "Bob says to himself, 'Hey!'"),
            (self.alice, "Bob says to himself, 'Hey!'"),
            ])

        msg_info = {}
        msg_info["msg_type"] = MsgType.action_say_to
        msg_info["actor"] = self.alice
        msg_info["recipients"] = [self.alice]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_action_msg(msg_info), [
            (self.bob, "Alice says to herself, 'Hey!'"),
            (self.tim, "Alice says to herself, 'Hey!'"),
            (self.alice, "You say to yourself, 'Hey!'"),
            ])

    def test_cant_hear(self):
        msg_info = {}
        msg_info["msg_type"] = MsgType.action_say_to
        msg_info["actor"] = self.bob
        msg_info["recipients"] = [self.tim]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_action_msg(msg_info), [
            (self.bob, "You say to Tim, 'Hey!'"),
            (self.tim, "Bob says to you, 'Hey!'"),
            (self.alice, "Bob says to Tim, 'Hey!'"),
            ])

        # Alice shouldn't hear anything
        add_status_effect(self.alice, Afflictions.deaf)
        self.assertEqual(format_action_msg(msg_info), [
            (self.bob, "You say to Tim, 'Hey!'"),
            (self.tim, "Bob says to you, 'Hey!'"),
            (self.alice, "You see Bob moving his lips but can't hear anything."),
            ])

    def test_cant_see(self):
        msg_info = {}
        msg_info["msg_type"] = MsgType.action_say_to
        msg_info["actor"] = self.bob
        msg_info["recipients"] = [self.tim]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_action_msg(msg_info), [
            (self.bob, "You say to Tim, 'Hey!'"),
            (self.tim, "Bob says to you, 'Hey!'"),
            (self.alice, "Bob says to Tim, 'Hey!'"),
            ])

        # Alice shouldn't hear anything
        add_status_effect(self.alice, Afflictions.blind)
        self.assertEqual(format_action_msg(msg_info), [
            (self.bob, "You say to Tim, 'Hey!'"),
            (self.tim, "Bob says to you, 'Hey!'"),
            (self.alice, "You hear someone say, 'Hey!'"),
            ])

    def test_blind_and_deaf(self):
        msg_info = {}
        msg_info["msg_type"] = MsgType.action_say_to
        msg_info["actor"] = self.bob
        msg_info["recipients"] = [self.tim]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_action_msg(msg_info), [
            (self.bob, "You say to Tim, 'Hey!'"),
            (self.tim, "Bob says to you, 'Hey!'"),
            (self.alice, "Bob says to Tim, 'Hey!'"),
            ])

        # Alice shouldn't hear anything
        add_status_effect(self.alice, Afflictions.blind)
        add_status_effect(self.alice, Afflictions.deaf)
        self.assertEqual(format_action_msg(msg_info), [
            (self.bob, "You say to Tim, 'Hey!'"),
            (self.tim, "Bob says to you, 'Hey!'"),
            ])


class FormatMsg(unittest.TestCase):

    def setUp(self):
        self.bob = play.make_bob()
        self.bob.comms = AI_IO(ai_name=self.bob.name, from_server_file="test/output/test_bob.txt")

        self.tim = play.make_tim()
        self.tim.comms = AI_IO(ai_name=self.tim.name, from_server_file="test/output/test_tim.txt")

        self.alice = play.make_alice()
        self.alice.comms = AI_IO(ai_name=self.alice.name,
            from_server_file="test/output/test_alice.txt")

    def test_uppercase_msg(self):
        msg_info = {}
        msg_info["msg_type"] = MsgType.action_say_to
        msg_info["actor"] = self.bob
        msg_info["recipients"] = [self.tim]
        msg_info["words"] = "Hey!"
        msg_info["entities"] = [self.bob, self.tim, self.alice]
        self.assertEqual(format_msg(msg_info), [
            (self.bob, "You say to Tim, 'Hey!'"),
            (self.tim, "Bob says to you, 'Hey!'"),
            (self.alice, "Bob says to Tim, 'Hey!'"),
            ])


if __name__ == '__main__':
    unittest.main()
