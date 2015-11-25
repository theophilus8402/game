#!/usr/bin/python3

import collections
from datetime import datetime
import select
import queue

import model.msg
import model.world
import control.comm
import control.mymap
import control.entity.ai
import control.entity.living
import play

CMDS_BASIC_MOVEMENT = {"n", "ne", "e", "se", "s", "sw", "w", "nw"}
CMDS_BASIC_ATTACK = {"hit", "fhit", "cast"}
CMDS_BASIC_HUMANOID = {"get", "eat", "drink", "wear", "wield", "remove",
    "unwield", "l", "look", "quit", "exit"}
CMDS_DEBUG = {"dist"}

def get_input_from_players(world, readable):
    for s in readable:
        src_ent = world.player_driven_comms[s]
        data = src_ent.comms.recv()
        if data:
            command = data.split()[0]
            if command in bob.known_cmds:
                new_msg = model.msg.ActionMsgs(cmd_word=command,
                    msg=data, src_entity=src_ent)
                world.immediate_action_msgs.put(new_msg)
            else:
                src_ent.comms.send("Huh? What is {}".format(command))


def get_input_from_ai(world):
    for ai in world.ai_entities:
        data = ai.comms.recv()
        if data:
            command = data.split()[0]
            if command in ai.known_cmds:
                new_msg = model.msg.ActionMsgs(cmd_word=command,
                    msg=data, src_entity=ai)
                world.immediate_action_msgs.put(new_msg)
            else:
                ai.comms.send("{} doesn't know how to {}...".format(
                    ai.name, command))


def handle_action_msgs(world):
    continue_loop = True
    msg_queue = world.immediate_action_msgs
    while not msg_queue.empty():
        msg = msg_queue.get()
        msg_text = msg.msg
        src_ent = msg.src_entity
        if msg_text == "exit":
            continue_loop = False
            src_ent.comms.send("Goodbye!  We'll miss you!")
        else:
            action = world.actions[msg.cmd_word]
            action(world, msg)
        #src_ent.comms.send(msg)     # this just shows what msg was sent
    return continue_loop


def run_ai(world):
    ai_input_msgs = []
    tim = world.find_entity("tim")
    if tim:
        msg = tim.run()
    return ai_input_msgs


def default_action(world, msg):
    msg.src_entity.comms.send("Unknown world action: \"{}\"?".format(msg.msg))


def move(world, msg):
    msg.src_entity.comms.send("Moving {}...".format(msg.cmd_word))


if __name__ == "__main__":

    world = play.make_world()
    world.actions = collections.defaultdict(lambda: default_action)
    world.actions["hit"] = control.entity.living.action_hit
    world.actions["fhit"] = control.entity.living.action_hit
    world.actions["n"] = move
    world.actions["e"] = move
    world.actions["s"] = move
    world.actions["w"] = move
    world.actions["dist"] = control.entity.living.action_show_distance
    world.actions["l"] = control.entity.living.action_look
    world.actions["look"] = control.entity.living.action_look
    world.player_driven_comms = {}
    world.immediate_action_msgs = queue.Queue()

    bob = play.make_bob()
    bob.comms = control.comm.File_IO()
    world.player_driven_comms[bob.comms.input_handle] = bob
    bob.known_cmds = CMDS_BASIC_MOVEMENT.union(CMDS_BASIC_ATTACK)
    bob.known_cmds = bob.known_cmds.union(CMDS_BASIC_HUMANOID)
    bob.known_cmds = bob.known_cmds.union(CMDS_DEBUG)
    model.entity.living.remove_status_msg(bob, "paralyzed")
    play.put(world, bob, (1, 0))
    print("cur_loc: {}".format(bob.cur_loc))

    tim = play.make_tim()
    Humanoid = model.entity.entity.Humanoid
    Humanoid.set_next_run_time = control.entity.ai.simple_set_next_run_time
    tim.cmd_interval = (0, 4)
    tim.set_next_run_time()
    Humanoid.get_next_cmd = control.entity.ai.simple_get_next_cmd
    Humanoid.run = control.entity.ai.simple_run
    tim.known_cmds = ["n", "e", "s", "w", "hit"]
    tim.run_cmds = ["n", "e", "s", "w", "hit bob"]
    """
    for i in range(5):
        print(tim.get_next_cmd())
    """
    tim.comms = control.comm.AI_IO(ai_name=tim.name)
    tim.comms.send("Hey, Tim!")
    world.ai_entities = [tim]
    play.put(world, tim, (0, 0))

    world.living_ents[bob.name] = bob
    world.living_ents[tim.name] = tim

    sword = play.make_sword()
    play.put(world, sword, (1, 1))

    control.mymap.display_map(world, bob)

    timeout = .1
    continue_loop = True
    while continue_loop:

        readable, writable, exceptional = select.select(
            world.player_driven_comms, [], [], timeout)

        get_input_from_players(world, readable)
        #get_input_from_ai(world)

        #run_ai(world)

        continue_loop = handle_action_msgs(world)
