#!/usr/bin/python3.4

import sys
from time import sleep
import unittest

from control.comm import *
from control.entity.living import *
from model.info import Status
from model.world import *
import play
from view import *

class Action_Say(unittest.TestCase):

    def setUp(self):
        self.world = play.make_world()

        self.bob = play.make_bob()
        self.bob.comms = AI_IO(ai_name=self.bob.name, from_server_file="test_bob.txt")
        add_entity(get_tile(self.world, Coord(1, 0)), self.bob)

        self.tim = play.make_tim()
        self.tim.comms = AI_IO(ai_name=self.tim.name, from_server_file="test_tim.txt")
        add_entity(get_tile(self.world, Coord(0, 0)), self.tim)

        self.alice = play.make_alice()
        self.alice.comms = AI_IO(ai_name=self.alice.name,
           from_server_file="test_alice.txt")
        add_entity(get_tile(self.world, Coord(2, 3)), self.alice)

        area_entity_check(self.world, self.bob)
        area_entity_check(self.world, self.tim)
        area_entity_check(self.world, self.alice)
 
    def test_say_simple(self):
        msg = ActionMsgs(cmd_word="say", msg="say hello", src_entity=self.bob)
        action_say(self.world, msg)
        self.assertEqual(self.bob.comms.read_from_server(), "You say, 'Hello'\n")
        self.assertEqual(self.tim.comms.read_from_server(), "Bob says, 'Hello'\n")
        self.assertEqual(self.alice.comms.read_from_server(), "Bob says, 'Hello'\n")
 
    def test_say_nothing(self):
        msg = ActionMsgs(cmd_word="say", msg="say ", src_entity=self.bob)
        action_say(self.world, msg)
        bobs_msg = self.bob.comms.read_from_server().strip()
        possible_msgs = error_code_msgs[Status.saying_nothing]
        self.assertTrue(bobs_msg in possible_msgs)
        self.assertEqual(self.tim.comms.read_from_server(), None)
        self.assertEqual(self.alice.comms.read_from_server(), None)

        msg = ActionMsgs(cmd_word="say", msg="say to tim ", src_entity=self.bob)
        action_say(self.world, msg)
        bobs_msg = self.bob.comms.read_from_server().strip()
        possible_msgs = error_code_msgs[Status.saying_nothing]
        self.assertTrue(bobs_msg in possible_msgs)
        self.assertEqual(self.tim.comms.read_from_server(), None)
        self.assertEqual(self.alice.comms.read_from_server(), None)

        msg = ActionMsgs(cmd_word="say", msg="say to tim", src_entity=self.bob)
        action_say(self.world, msg)
        bobs_msg = self.bob.comms.read_from_server().strip()
        possible_msgs = error_code_msgs[Status.saying_nothing]
        self.assertTrue(bobs_msg in possible_msgs)
        self.assertEqual(self.tim.comms.read_from_server(), None)
        self.assertEqual(self.alice.comms.read_from_server(), None)

        msg = ActionMsgs(cmd_word="say", msg="say to ", src_entity=self.bob)
        action_say(self.world, msg)
        self.assertEqual(self.bob.comms.read_from_server(), "You say, 'To'\n")
        self.assertEqual(self.tim.comms.read_from_server(), "Bob says, 'To'\n")
        self.assertEqual(self.alice.comms.read_from_server(), "Bob says, 'To'\n")

    def test_say_bad_entity(self):
        msg = ActionMsgs(cmd_word="say", msg="say to phil Hey", src_entity=self.bob)
        action_say(self.world, msg)
        bobs_msg = self.bob.comms.read_from_server().strip()
        possible_msgs = error_code_msgs[Status.target_doesnt_exist]
        self.assertTrue(bobs_msg in possible_msgs)


class AllowedTo(unittest.TestCase):

    def setUp(self):
        self.world = play.make_world()

        self.bob = play.make_bob()
        self.bob.comms = AI_IO(ai_name=self.bob.name, from_server_file="test_bob.txt")
        add_entity(get_tile(self.world, Coord(1, 0)), self.bob)

        self.tim = play.make_tim()
        self.tim.comms = AI_IO(ai_name=self.tim.name, from_server_file="test_tim.txt")
        add_entity(get_tile(self.world, Coord(0, 0)), self.tim)

        self.alice = play.make_alice()
        self.alice.comms = AI_IO(ai_name=self.alice.name,
           from_server_file="test_alice.txt")
        add_entity(get_tile(self.world, Coord(2, 3)), self.alice)

        area_entity_check(self.world, self.bob)
        area_entity_check(self.world, self.tim)
        area_entity_check(self.world, self.alice)
 
    def test_allowed_to_attack(self):
        self.assertTrue(allowed_to_attack(self.bob))

        # bob get's only one attack, see if he can attack again
        self.bob.round_info.num_attacks += 1
        self.assertFalse(allowed_to_attack(self.bob))

        # see if he can attack now
        self.bob.max_num_attacks = 3
        self.assertTrue(allowed_to_attack(self.bob))

        # see if he can attack after having moved past his speed
        self.bob.round_info.feet_moved = 31
        self.assertFalse(allowed_to_attack(self.bob))

        # wait for the round to end and then see if we can attack
        #sleep(4)
        #self.assertTrue(allowed_to_attack(self.bob))

        self.bob.round_info.other_action = True
        #print(self.bob.round_info)
        self.assertFalse(allowed_to_attack(self.bob))
        #if self.bob.round_info.other_action:
        #    print("Hrm... this should have failed earlier...")
        

    def test_allowed_to_move(self):
        self.assertFalse(True)


class FormatAndSendMsg(unittest.TestCase):

    def setUp(self):
        self.world = play.make_world()

        self.bob = play.make_bob()
        self.bob.comms = AI_IO(ai_name=self.bob.name, from_server_file="test_bob.txt")
        add_entity(get_tile(self.world, Coord(1, 0)), self.bob)

        self.tim = play.make_tim()
        self.tim.comms = AI_IO(ai_name=self.tim.name, from_server_file="test_tim.txt")
        add_entity(get_tile(self.world, Coord(0, 0)), self.tim)

        self.alice = play.make_alice()
        self.alice.comms = AI_IO(ai_name=self.alice.name,
           from_server_file="test_alice.txt")
        add_entity(get_tile(self.world, Coord(2, 3)), self.alice)

        area_entity_check(self.world, self.bob)
        area_entity_check(self.world, self.tim)
        area_entity_check(self.world, self.alice)

    def test_format_and_send_msg(self):
        peeps_nearby = [self.bob]
        peeps_nearby.extend(self.bob.peeps_nearby)
        msg_info = {
            "msg_type"  :   MsgType.action_hit,
            "actor"     :   self.bob,
            "recipients":   [self.tim],
            "entities"  :   peeps_nearby,
            }

        msg_info["dmg"] = 5
        format_and_send_msg(msg_info)
        self.assertEqual(self.bob.comms.read_from_server(),
            "You maliciously hit tim!\n")
        self.assertEqual(self.tim.comms.read_from_server(),
            "Bob maliciously hit you!\n")
        self.assertEqual(self.alice.comms.read_from_server(),
            "Bob maliciously hit tim!\n")

    def test_send_error_msg(self):
        peeps_nearby = [self.bob]
        peeps_nearby.extend(self.bob.peeps_nearby)
        msg_info = {
            "msg_type"  :   MsgType.action_hit,
            "actor"     :   self.bob,
            "recipients":   [self.tim],
            "entities"  :   peeps_nearby,
            }

        send_error_msg(msg_info, Status.cant_do_this_round)
        possible_msgs = error_code_msgs[Status.cant_do_this_round]
        msg = self.bob.comms.read_from_server().strip()
        self.assertTrue(msg in possible_msgs)


        send_error_msg(msg_info, Status.incorrect_syntax)
        possible_msgs = error_code_msgs[Status.incorrect_syntax]
        msg = self.bob.comms.read_from_server().strip()
        self.assertTrue(msg in possible_msgs)


        send_error_msg(msg_info, Status.target_doesnt_exist)
        possible_msgs = error_code_msgs[Status.target_doesnt_exist]
        msg = self.bob.comms.read_from_server().strip()
        self.assertTrue(msg in possible_msgs)


        send_error_msg(msg_info, Status.target_too_far_away)
        possible_msgs = error_code_msgs[Status.target_too_far_away]
        msg = self.bob.comms.read_from_server().strip()
        self.assertTrue(msg in possible_msgs)


        msg_info["affliction"] = Afflictions.paralysis
        send_error_msg(msg_info, Status.impeding_affliction)
        possible_msgs = error_code_msgs[Status.impeding_affliction]
        formatted_possible_msgs = []
        for pmsg in possible_msgs:
            formatted_possible_msgs.append(pmsg.format(**msg_info))
        msg = self.bob.comms.read_from_server().strip()
        print(msg)
        print(formatted_possible_msgs)
        self.assertTrue(msg in formatted_possible_msgs)


class ActionHit(unittest.TestCase):

    def setUp(self):
        self.world = play.make_world()

        self.bob = play.make_bob()
        self.bob.comms = AI_IO(ai_name=self.bob.name, from_server_file="test_bob.txt")
        add_entity(get_tile(self.world, Coord(1, 0)), self.bob)

        self.sword = play.make_sword()
        self.bob.eq[Body.right_arm] = self.sword

        self.tim = play.make_tim()
        self.tim.comms = AI_IO(ai_name=self.tim.name, from_server_file="test_tim.txt")
        add_entity(get_tile(self.world, Coord(0, 0)), self.tim)

        self.alice = play.make_alice()
        self.alice.comms = AI_IO(ai_name=self.alice.name,
           from_server_file="test_alice.txt")
        add_entity(get_tile(self.world, Coord(2, 3)), self.alice)

        self.world.living_ents[self.bob.name] = self.bob
        self.world.living_ents[self.tim.name] = self.tim
        self.world.living_ents[self.alice.name] = self.alice

        area_entity_check(self.world, self.bob)
        area_entity_check(self.world, self.tim)
        area_entity_check(self.world, self.alice)


    def test_action_hit(self):
        # should fail on actions that can be taken this round
        self.bob.round_info.other_action = True
        msg = ActionMsgs(cmd_word="hit", msg="hit tim", src_entity=self.bob)
        self.assertEqual(action_hit(self.world, msg), Status.cant_do_this_round)
        self.bob.round_info.other_action = False

        msg = self.bob.comms.read_from_server().strip()
        #print(msg)

        # should fail on incorrect syntax
        msg = ActionMsgs(cmd_word="hit", msg="hit tim now", src_entity=self.bob)
        self.assertEqual(action_hit(self.world, msg), Status.incorrect_syntax)

        msg = self.bob.comms.read_from_server().strip()
        #print(msg)

        # should fail on entity non-existant
        msg = ActionMsgs(cmd_word="hit", msg="hit phil", src_entity=self.bob)
        self.assertEqual(action_hit(self.world, msg), Status.target_doesnt_exist)

        msg = self.bob.comms.read_from_server().strip()
        #print(msg)

        # should fail on entity too far
        msg = ActionMsgs(cmd_word="hit", msg="hit alice", src_entity=self.bob)
        self.assertEqual(action_hit(self.world, msg), Status.target_doesnt_exist)

        # should fail on entity affliction
        add_status_effect(self.bob, Afflictions.paralysis)
        msg = ActionMsgs(cmd_word="hit", msg="hit tim", src_entity=self.bob)
        self.assertEqual(action_hit(self.world, msg), Status.impeding_affliction)
        remove_status_effect(self.bob, Afflictions.paralysis)

        msg = self.bob.comms.read_from_server().strip()
        #print(msg)

        # should miss attack
        self.tim.ac = 34
        msg = ActionMsgs(cmd_word="hit", msg="hit tim", src_entity=self.bob)
        self.assertEqual(action_hit(self.world, msg), Status.attack_missed)

        # should fail because of not being attack enough times this round (i.e. once)
        msg = ActionMsgs(cmd_word="hit", msg="hit tim", src_entity=self.bob)
        self.assertEqual(action_hit(self.world, msg), Status.cant_do_this_round)

        # should hit all the time because tim has an ac of 1
        self.bob.max_num_attacks = 4
        self.tim.ac = 1
        msg = ActionMsgs(cmd_word="hit", msg="hit tim", src_entity=self.bob)
        self.assertEqual(action_hit(self.world, msg), Status.all_good)


if __name__ == '__main__':
    unittest.main()
