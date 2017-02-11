#!/usr/bin/python3

import collections
import select
import sys
import queue

from control.world import world_get_input
import control.comm
from model.world import get_tile, area_entity_check
from model.tile import Coord, tile_add_entity
from model.entity.living import *
from model.entity.living.status_effects import Body, add_status_effect, Blessings
import control.entity.ai
from control.entity.living import default_world_actions
import play


if __name__ == "__main__":

    world = play.make_world()
    world.actions = default_world_actions
    world.socket_entity_map = {}
    world.immediate_action_msgs = queue.Queue()

    bob = play.make_bob()
    add_status_effect(bob, Blessings.game_master)
    bob.comms = control.comm.Std_IO()
    world.socket_entity_map[bob.comms.input_handle] = bob
    tile_add_entity(get_tile(world, Coord(1, 0)), bob)
    print("bob's current coord: {}".format(bob.coord))

    tim = play.make_tim()
    """
    ai_tim = control.entity.ai.Simple_AI(tim)
    ai_tim.run_cmds = ["n", "e", "s", "w", "hit bob"]
    tim.comms = control.comm.AI_IO(ai_name=tim.name, from_server_file="tim.txt")
    tim.comms.send("Hey, Tim!")
    world.socket_entity_map[tim.comms.server_read_handle] = tim
    world.ai_entities = [ai_tim]
    tile_add_entity(get_tile(world, Coord(0, 0)), tim)
    """

    dog = play.make_dog()
    ai_dog = control.entity.ai.Simple_AI(dog)
    ai_dog.cmd_interval = (5, 10)
    #ai_dog.run_cmds = ["n", "ne", "e", "se", "s", "sw", "w", "nw", "say bark"]
    ai_dog.run_cmds = ["say bark"]
    dog.comms = control.comm.AI_IO(ai_name=dog.name, from_server_file="dog.txt")
    world.socket_entity_map[dog.comms.server_read_handle] = dog
    world.ai_entities.append(ai_dog)
    tile_add_entity(get_tile(world, Coord(2, 3)), dog)

    alice = play.make_alice()

    world.living_ents[bob.name.lower()] = bob
    world.living_ents[tim.name.lower()] = tim
    world.living_ents[dog.name.lower()] = dog
    world.living_ents[alice.name.lower()] = alice

    sword = play.make_sword()
    armour = play.make_armour()
    tile_add_entity(get_tile(world, Coord(-1, -1)), armour)
    shoe = play.make_shoes()
    tile_add_entity(get_tile(world, Coord(-1, -1)), shoe)
    #tile_add_entity(get_tile(world, Coord(1, 1)), sword)
    bob.eq[Body.right_arm] = sword

    area_entity_check(world, bob)
    #print("peeps nearby: {}".format(bob.peeps_nearby))
    #area_entity_check(world, tim)
    #print("peeps nearby: {}".format(tim.peeps_nearby))
    area_entity_check(world, dog)
    #print("peeps nearby: {}".format(dog.peeps_nearby))

    control.comm.start_server(world, "", 2222)

    timeout = .1
    continue_loop = True
    while continue_loop:

        readable, writable, exceptional = select.select(
            world.socket_entity_map, [], [], timeout)

        world_get_input(world, readable)

        control.entity.living.run_ai(world)

        continue_loop = control.entity.living.handle_action_msgs(world)
