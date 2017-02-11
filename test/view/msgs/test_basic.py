#!/usr/bin/python3.4

from collections import defaultdict
import unittest
import sys

from model.entity.living.status_effects import *
from model.entity.living.equip import EqSlots
from view.msgs.basic import *
import play


class BasicFormatFuncs(unittest.TestCase):

    def setUp(self):
        self.bob = play.make_bob()
        self.tim = play.make_tim()

    def test_format_actor(self):
        info = {"actor" : self.bob}
        self.assertEqual(format_actor(info, self.tim), "Bob")
        self.assertEqual(format_actor(info, self.bob), "you")
        self.assertEqual(format_actor(info, self.bob, capitalize=True), "You")
        self.assertEqual(format_actor(info, self.tim, capitalize=True), "Bob")
        self.assertEqual(format_map["Actor"](info, self.bob), "You")
        self.assertEqual(format_map["actor"](info, self.bob), "you")
        self.assertEqual(format_map["actor"](info, self.tim), "Bob")


class TestUnformattedMsg(unittest.TestCase):

    def setUp(self):
        self.bob = play.make_bob()
        self.tim = play.make_tim()
        self.plate = play.make_armour()
        unf_msg_str = "{Actor} {action_wear} {item} on {actor_poss} {eq_slot}."
        self.msg1 = UnformattedMsg([unf_msg_str], can_be_deaf=True)

    def test_unformatted_msg(self):
        self.assertEqual(self.msg1.fields, ["Actor", "action_wear", "item",
            "actor_poss", "eq_slot"])
        self.assertEqual(self.msg1.can_be_deaf, True)
        self.assertEqual(self.msg1.can_be_blind, False)

    def test_format_msg(self):
        unf_msg_str = "{Actor} {action_wear} {item} on {actor_poss} {eq_slot}."
        info = {
            "actor"     : self.bob,
            "item" : self.plate,
            "eq_slot"   : EqSlots.torso,
            }
        formatted_msg = self.msg1.format_msg(info, self.bob)
        self.assertEqual(formatted_msg, "You wear a plate on your torso.")


class TestViewMsgManager(unittest.TestCase):

    def setUp(self):
        #unf_msg_str = "{Actor} {action_wear} {item} on {actor_poss} {eq_slot}."
        #self.wear_msg = UnformattedMsg([unf_msg_str], can_be_deaf=True)

        say_healthy_str = "{Actor} {action_say}, '{words}'"
        self.say_healthy_msg = UnformattedMsg([say_healthy_str])

        say_deaf_str = "You see {actor} moving {actor_poss} lips"\
            + " but can't hear anything."
        self.say_deaf_msg = UnformattedMsg([say_deaf_str], can_be_deaf=True)

        say_blind_str = "You hear someone say, '{words}'"
        self.say_blind_msg = UnformattedMsg([say_blind_str], can_be_blind=True)

        self.say_manager = ViewMsgManager()
        self.say_manager.add_msgs([self.say_healthy_msg, self.say_deaf_msg,
            self.say_blind_msg])

        self.bob = play.make_bob()
        self.tim = play.make_tim()
        self.dog = play.make_dog()

    def test_add_msgs(self):
        self.assertEqual(self.say_manager.view_msgs, [self.say_healthy_msg,
            self.say_deaf_msg, self.say_blind_msg])

    def test_get_unformatted_msg(self):
        unf_msg = self.say_manager.get_unformatted_msg(self.bob, self.tim, None)
        self.assertEqual(unf_msg, self.say_healthy_msg)

        add_status_effect(self.tim, Afflictions.blind)
        unf_msg = self.say_manager.get_unformatted_msg(self.bob, self.tim, None)
        self.assertEqual(unf_msg, self.say_blind_msg)

        remove_status_effect(self.tim, Afflictions.blind)
        add_status_effect(self.tim, Afflictions.deaf)
        unf_msg = self.say_manager.get_unformatted_msg(self.bob, self.tim, None)
        self.assertEqual(unf_msg, self.say_deaf_msg)

        add_status_effect(self.tim, Afflictions.blind)
        unf_msg = self.say_manager.get_unformatted_msg(self.bob, self.tim, None)
        self.assertEqual(unf_msg, None)

        remove_status_effect(self.tim, Afflictions.deaf)
        remove_status_effect(self.tim, Afflictions.blind)
        unf_msg = self.say_manager.get_unformatted_msg(self.bob, self.tim, None)
        self.assertEqual(unf_msg, self.say_healthy_msg)

        add_status_effect(self.bob, Afflictions.blind)
        unf_msg = self.say_manager.get_unformatted_msg(self.bob, self.tim, None)
        self.assertEqual(unf_msg, self.say_healthy_msg)

    def test_format_msgs(self):
        info = {
            "actor" : self.bob,
            "words" : "Hello",
            "entities" : [self.bob, self.tim],
            "msg_type" : MsgType.action_say,
            }
        fmsgs = self.say_manager.format_msgs(info)
        self.assertEqual((self.bob, "You say, 'Hello'"), fmsgs[0])
        self.assertEqual((self.tim, "Bob says, 'Hello'"), fmsgs[1])

        add_status_effect(self.tim, Afflictions.blind)
        fmsgs = action_say_msg_manager.format_msgs(info)
        self.assertEqual((self.bob, "You say, 'Hello'"), fmsgs[0])
        self.assertEqual((self.tim, "You hear someone say, 'Hello'"), fmsgs[1])
        remove_status_effect(self.tim, Afflictions.blind)

        add_status_effect(self.tim, Afflictions.deaf)
        fmsgs = action_say_msg_manager.format_msgs(info)
        self.assertEqual((self.bob, "You say, 'Hello'"), fmsgs[0])
        self.assertEqual((self.tim,
            "You see Bob moving his lips but can't hear anything."),
            fmsgs[1])
        remove_status_effect(self.tim, Afflictions.deaf)

        add_status_effect(self.tim, Afflictions.deaf)
        add_status_effect(self.tim, Afflictions.blind)
        fmsgs = action_say_msg_manager.format_msgs(info)
        self.assertEqual((self.bob, "You say, 'Hello'"), fmsgs[0])
        remove_status_effect(self.tim, Afflictions.deaf)
        remove_status_effect(self.tim, Afflictions.blind)


        info = {
            "actor" : self.bob,
            "entities" : [self.bob, self.tim],
            "recip" : self.tim,
            "msg_type" : MsgType.action_hit,
            }
        fmsgs = action_hit_msg_manager.format_msgs(info)
        self.assertEqual((self.bob, "You maliciously hit Tim!"), fmsgs[0])
        self.assertEqual((self.tim, "Bob maliciously hits you!"), fmsgs[1])

        add_status_effect(self.tim, Afflictions.deaf)
        fmsgs = action_hit_msg_manager.format_msgs(info)
        self.assertEqual((self.bob, "You maliciously hit Tim!"), fmsgs[0])
        self.assertEqual((self.tim, "Bob maliciously hits you!"), fmsgs[1])
        remove_status_effect(self.tim, Afflictions.deaf)

        add_status_effect(self.tim, Afflictions.blind)
        fmsgs = action_hit_msg_manager.format_msgs(info)
        self.assertEqual((self.bob, "You maliciously hit Tim!"), fmsgs[0])
        self.assertEqual((self.tim, "Someone hit you!"), fmsgs[1])
        remove_status_effect(self.tim, Afflictions.blind)

        add_status_effect(self.tim, Afflictions.deaf)
        add_status_effect(self.tim, Afflictions.blind)
        fmsgs = action_hit_msg_manager.format_msgs(info)
        self.assertEqual((self.bob, "You maliciously hit Tim!"), fmsgs[0])
        self.assertEqual((self.tim, "Someone hit you!"), fmsgs[1])
        remove_status_effect(self.tim, Afflictions.deaf)
        remove_status_effect(self.tim, Afflictions.blind)


        info = {
            "actor" : self.bob,
            "entities" : [self.bob, self.tim, self.dog],
            "recip" : self.dog,
            "msg_type" : MsgType.action_hit,
            }
        fmsgs = action_hit_msg_manager.format_msgs(info)
        self.assertEqual((self.bob, "You maliciously hit dog!"), fmsgs[0])
        self.assertEqual((self.tim, "Bob maliciously hits dog!"), fmsgs[1])
        self.assertEqual((self.dog, "Bob maliciously hits you!"), fmsgs[2])

        add_status_effect(self.tim, Afflictions.deaf)
        fmsgs = action_hit_msg_manager.format_msgs(info)
        self.assertEqual((self.bob, "You maliciously hit dog!"), fmsgs[0])
        self.assertEqual((self.tim, "Bob maliciously hits dog!"), fmsgs[1])
        self.assertEqual((self.dog, "Bob maliciously hits you!"), fmsgs[2])
        remove_status_effect(self.tim, Afflictions.deaf)

        add_status_effect(self.tim, Afflictions.blind)
        fmsgs = action_hit_msg_manager.format_msgs(info)
        self.assertEqual((self.bob, "You maliciously hit dog!"), fmsgs[0])
        self.assertEqual((self.tim, "You hear some fighting going on nearby."), fmsgs[1])
        self.assertEqual((self.dog, "Bob maliciously hits you!"), fmsgs[2])
        remove_status_effect(self.tim, Afflictions.blind)

        add_status_effect(self.tim, Afflictions.deaf)
        add_status_effect(self.tim, Afflictions.blind)
        fmsgs = action_hit_msg_manager.format_msgs(info)
        self.assertEqual((self.bob, "You maliciously hit dog!"), fmsgs[0])
        # tim is skipped because he shouldn't get a msg
        self.assertEqual((self.dog, "Bob maliciously hits you!"), fmsgs[1])
        remove_status_effect(self.tim, Afflictions.deaf)
        remove_status_effect(self.tim, Afflictions.blind)


if __name__ == '__main__':
    unittest.main()
