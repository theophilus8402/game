#!/usr/bin/python3.4

import sys
from time import sleep
import unittest

from control.comm import *
from control.entity.living import *
from model.info import Status
from model.world import *
from model.entity.inventory import *
import play
from view import *

class ActionSay(unittest.TestCase):

    def setUp(self):
        self.world = play.make_world()

        self.bob = play.make_bob()
        self.bob.comms = AI_IO(ai_name=self.bob.name, from_server_file="test/output/test_bob.txt")
        tile_add_entity(get_tile(self.world, Coord(1, 0)), self.bob)

        self.tim = play.make_tim()
        self.tim.comms = AI_IO(ai_name=self.tim.name, from_server_file="test/output/test_tim.txt")
        tile_add_entity(get_tile(self.world, Coord(0, 0)), self.tim)

        self.alice = play.make_alice()
        self.alice.comms = AI_IO(ai_name=self.alice.name,
           from_server_file="test/output/test_alice.txt")
        tile_add_entity(get_tile(self.world, Coord(2, 3)), self.alice)

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
        self.bob.comms = AI_IO(ai_name=self.bob.name, from_server_file="test/output/test_bob.txt")
        tile_add_entity(get_tile(self.world, Coord(1, 0)), self.bob)

        self.tim = play.make_tim()
        self.tim.comms = AI_IO(ai_name=self.tim.name, from_server_file="test/output/test_tim.txt")
        tile_add_entity(get_tile(self.world, Coord(0, 0)), self.tim)

        self.alice = play.make_alice()
        self.alice.comms = AI_IO(ai_name=self.alice.name,
           from_server_file="test/output/test_alice.txt")
        tile_add_entity(get_tile(self.world, Coord(2, 3)), self.alice)

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
        self.bob.comms = AI_IO(ai_name=self.bob.name, from_server_file="test/output/test_bob.txt")
        tile_add_entity(get_tile(self.world, Coord(1, 0)), self.bob)

        self.tim = play.make_tim()
        self.tim.comms = AI_IO(ai_name=self.tim.name, from_server_file="test/output/test_tim.txt")
        tile_add_entity(get_tile(self.world, Coord(0, 0)), self.tim)

        self.alice = play.make_alice()
        self.alice.comms = AI_IO(ai_name=self.alice.name,
           from_server_file="test/output/test_alice.txt")
        tile_add_entity(get_tile(self.world, Coord(2, 3)), self.alice)

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
            "You maliciously hit Tim!\n")
        self.assertEqual(self.tim.comms.read_from_server(),
            "Bob maliciously hits you!\n")
        self.assertEqual(self.alice.comms.read_from_server(),
            "Bob maliciously hits Tim!\n")

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


        msg_info["afflictions"] = {Afflictions.paralysis}
        send_error_msg(msg_info, Status.impeding_affliction)
        possible_msgs = error_code_msgs[Status.impeding_affliction]
        formatted_possible_msgs = []
        formatted_msg_info = make_format_string_dict(msg_info, self.bob)
        for pmsg in possible_msgs:
            formatted_possible_msgs.append(pmsg.format(**formatted_msg_info))
        msg = self.bob.comms.read_from_server().strip()
        #print(msg)
        #print(formatted_possible_msgs)
        self.assertTrue(msg in formatted_possible_msgs)


class ActionHit(unittest.TestCase):

    def setUp(self):
        self.world = play.make_world()

        self.bob = play.make_bob()
        self.bob.comms = AI_IO(ai_name=self.bob.name, from_server_file="test/output/test_bob.txt")
        tile_add_entity(get_tile(self.world, Coord(1, 0)), self.bob)

        self.sword = play.make_sword()
        self.bob.eq[Body.right_arm] = self.sword

        self.tim = play.make_tim()
        self.tim.comms = AI_IO(ai_name=self.tim.name, from_server_file="test/output/test_tim.txt")
        tile_add_entity(get_tile(self.world, Coord(0, 0)), self.tim)

        self.alice = play.make_alice()
        self.alice.comms = AI_IO(ai_name=self.alice.name,
           from_server_file="test/output/test_alice.txt")
        tile_add_entity(get_tile(self.world, Coord(2, 3)), self.alice)

        self.world.living_ents[self.bob.name.lower()] = self.bob
        self.world.living_ents[self.tim.name.lower()] = self.tim
        self.world.living_ents[self.alice.name.lower()] = self.alice

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


class ActionLookHere(unittest.TestCase):

    def setUp(self):
        self.world = play.make_world()

        self.bob = play.make_bob()
        self.bob.comms = AI_IO(ai_name=self.bob.name, from_server_file="test/output/test_bob.txt")
        self.bob_tile = get_tile(self.world, Coord(1, 0))
        tile_add_entity(self.bob_tile, self.bob)

        self.sword = play.make_sword()
        tile_add_entity(self.bob_tile, self.sword)

        self.tim = play.make_tim()
        self.tim.comms = AI_IO(ai_name=self.tim.name, from_server_file="test/output/test_tim.txt")
        tile_add_entity(get_tile(self.world, Coord(0, 0)), self.tim)

        self.armour = play.make_armour()
        tile_add_entity(get_tile(self.world, Coord(0, 0)), self.armour)

        self.shoe = play.make_shoe()
        tile_add_entity(get_tile(self.world, Coord(0, 0)), self.shoe)

        self.world.living_ents[self.bob.name.lower()] = self.bob
        self.world.living_ents[self.tim.name.lower()] = self.tim

        area_entity_check(self.world, self.bob)
        area_entity_check(self.world, self.tim)

    def test_healthy_look_here(self):
        msg = ActionMsgs(cmd_word="lh", msg="lh", src_entity=self.bob)
        self.assertEqual(action_look_here(self.world, msg), Status.all_good)
        recv_msg = self.bob.comms.read_from_server()
        entities = ["{}{}".format(TAB, ent) for ent in ["short sword"]]
        should_be_msg = unformatted_msgs[MsgType.action_look_here][EntStatus.healthy]
        should_be_msg = should_be_msg[0].format(tile_entities="".join(entities))
        self.assertEqual(recv_msg.rstrip(), should_be_msg.replace("\n", ""))

        msg = ActionMsgs(cmd_word="lh", msg="lh", src_entity=self.tim)
        self.assertEqual(action_look_here(self.world, msg), Status.all_good)
        recv_msg = self.tim.comms.read_from_server()
        entities = ["{}{}".format(TAB, ent) for ent in ["plate", "shoe"]]
        should_be_msg = unformatted_msgs[MsgType.action_look_here][EntStatus.healthy]
        should_be_msg = should_be_msg[0].format(tile_entities="".join(entities))
        self.assertEqual(recv_msg.rstrip(), should_be_msg.replace("\n", ""))

        add_status_effect(self.tim, Afflictions.blind)
        msg = ActionMsgs(cmd_word="lh", msg="lh", src_entity=self.tim)
        self.assertEqual(action_look_here(self.world, msg), Status.impeding_affliction)
        recv_msg = self.tim.comms.read_from_server()
        possible_unformatted_msgs = error_code_msgs[Status.impeding_affliction]
        info = {"afflictions" : {Afflictions.blind}}
        fsd = make_format_string_dict(info, self.tim)
        possible_msgs = [msg.format(**fsd).replace("\n", "")
                            for msg in possible_unformatted_msgs]
        self.assertTrue(recv_msg.rstrip() in possible_msgs)


class ActionGet(unittest.TestCase):

    def setUp(self):
        self.world = play.make_world()

        self.bob = play.make_bob()
        self.bob.comms = AI_IO(ai_name=self.bob.name, from_server_file="test/output/test_bob.txt")
        self.bob_tile = get_tile(self.world, Coord(1, 0))
        tile_add_entity(self.bob_tile, self.bob)

        self.sword = play.make_sword()
        tile_add_entity(self.bob_tile, self.sword)
        self.armour = play.make_armour()
        tile_add_entity(self.bob_tile, self.armour)

        self.tim = play.make_tim()
        self.tim.comms = AI_IO(ai_name=self.tim.name, from_server_file="test/output/test_tim.txt")
        self.tim_tile = get_tile(self.world, Coord(0, 0))
        tile_add_entity(self.tim_tile, self.tim)

        self.shoe = play.make_shoe()
        tile_add_entity(self.tim_tile, self.shoe)

        self.world.living_ents[self.bob.name.lower()] = self.bob
        self.world.living_ents[self.tim.name.lower()] = self.tim

        area_entity_check(self.world, self.bob)
        area_entity_check(self.world, self.tim)

    def test_no_item(self):
        # make sure the entity specified an item
        msg = ActionMsgs(cmd_word="get", msg="get", src_entity=self.bob)
        self.assertEqual(action_get(self.world, msg), Status.getting_nothing)
        msg = ActionMsgs(cmd_word="get", msg="get ", src_entity=self.bob)
        self.assertEqual(action_get(self.world, msg), Status.getting_nothing)
        #TODO: check msgs

        # make sure the item exists and is in the same tile as the entity
        msg = ActionMsgs(cmd_word="get", msg="get brusselsprouts", src_entity=self.bob)
        self.assertEqual(action_get(self.world, msg), Status.target_doesnt_exist)
        #TODO: check msgs

        # make sure the entity can make this action this round
        msg = ActionMsgs(cmd_word="get", msg="get short sword", src_entity=self.bob)
        self.assertEqual(action_get(self.world, msg), Status.all_good)
        msg = ActionMsgs(cmd_word="get", msg="get plate", src_entity=self.bob)
        self.assertEqual(action_get(self.world, msg), Status.cant_do_this_round)
        #TODO: check msgs

        # make sure the entity is physically capable of picking up the item
        #TODO: make some way of keeping track of items interacted with
        #TODO: make it so bob can pickup an item again
        add_status_effect(self.tim, Afflictions.lost_balance)
        msg = ActionMsgs(cmd_word="get", msg="get shoe", src_entity=self.tim)
        self.assertEqual(action_get(self.world, msg), Status.impeding_affliction)
        #TODO: check msgs
        remove_status_effect(self.tim, Afflictions.lost_balance)
        msg = ActionMsgs(cmd_word="get", msg="get shoe", src_entity=self.tim)
        self.assertEqual(action_get(self.world, msg), Status.all_good)

        # make sure bob has a sword but not the plate
        self.assertEqual(self.sword,
            inventory_find_item(self.bob.inventory, "short sword"))
        self.assertEqual(None, inventory_find_item(self.bob.inventory, "plate"))
        self.assertEqual(self.shoe, inventory_find_item(self.tim.inventory, "shoe"))
        #TODO: check msgs


if __name__ == '__main__':
    unittest.main()
