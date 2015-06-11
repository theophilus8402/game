#!/usr/bin/python3.4

import control.move
import control.roll
import control.admin
import control.socks
import control.mymap
import curses
import re

re_hit = re.compile("hit (?P<who>\w+)")
re_make_tile = re.compile("make tile \(([-0-9]+), ([-0-9]+)\) ?(\d+x\d+)?")

def find_entity_in_tile(target_name, entities):
    the_entity = None
    for entity in entities:
        if target_name.lower() == entity.name.lower():
            the_entity = entity
            break
    return the_entity

def find_target_nearby(world, bob, target_name):
    x, y = bob.cur_loc
    n = (0, 1)
    ne = (1, 1)
    e = (1, 0)
    se = (1, -1)
    s = (0, -1)
    sw = (-1, -1)
    w = (-1, 0)
    nw = (-1, 1)
    directions = [n, ne, e, se, s, sw, w, nw]
    target = None
    for mod_x, mod_y in directions:
        try:
            target = find_entity_in_tile(target_name,
                world.tiles[(x+mod_x, y+mod_y)].entities)
            if target:
                break
        except:
            target = None
    return target

def handle_user_input(world, bob, msg):

    should_exit = False

    if msg == "exit":
        should_exit = True
        control.socks.send_msg(world, bob,
            "Well, we'll miss you!  Goodbye!")
        control.socks.actually_send_msgs(world, bob)
        control.socks.remove_connection(world, bob.sock)
    elif bob.special_state:
        if bob.state == "login":
            control.socks.login(world, bob, msg)
        control.socks.send_msg(world, bob, "still in a special state")
    elif re_hit.match(msg):
        result = re_hit.match(msg)
        target_name = result.group("who")
        control.socks.send_msg(world, bob,
            "You want to hit {}?!".format(target_name))
        attack_roll = control.roll.roll(2, 6, 1)
        control.socks.send_msg(world, bob,
            "Attack roll: {}".format(attack_roll))
        dmg_roll = control.roll.roll(1, 6, 2)
        control.socks.send_msg(world, bob, "Dmg roll: {}".format(dmg_roll))

        # find the target nearby
        target_entity = find_target_nearby(world, bob, target_name)
        if target_entity:
            control.socks.send_msg(world, bob,
                "Found him at {}".format(target_entity.cur_loc))
            # apply dmg
            target_entity.cur_hp = target_entity.cur_hp - dmg_roll
            if target_entity.cur_hp <= 0:
                control.socks.send_msg(world, bob, "You killed {}!".format(
                    target_name))
                control.mymap.kill_creature(world, bob, target_entity)
        else:
            control.socks.send_msg(world, bob, "Couldn't find him...")
    elif re_make_tile.match(msg):
        result = re_make_tile.match(msg)
        x = int(result.group(1))
        y = int(result.group(2))
        coord = (x, y)
        dimensions = result.group(3)
        #dimensions = None
        control.admin.make_tile(world, bob, coord, dimensions)
    elif msg == "n":
        x, y = bob.cur_loc
        try:
            control.move.move(world, bob, (x,y), (x,y+1))
            control.mymap.display_map(world, bob)
            control.socks.send_msg(world, bob,
                "Now at: {}".format(bob.cur_loc))
        except:
            pass
    elif msg == "e":
        x, y = bob.cur_loc
        try:
            control.move.move(world, bob, (x,y), (x+1,y))
            control.mymap.display_map(world, bob)
            control.socks.send_msg(world, bob,
                "Now at: {}".format(bob.cur_loc))
        except:
            pass
    elif msg == "s":
        x, y = bob.cur_loc
        try:
            control.move.move(world, bob, (x,y), (x,y-1))
            control.mymap.display_map(world, bob)
            control.socks.send_msg(world, bob,
                "Now at: {}".format(bob.cur_loc))
        except:
            pass
    elif msg == "w":
        x, y = bob.cur_loc
        try:
            control.move.move(world, bob, (x,y), (x-1,y))
            control.mymap.display_map(world, bob)
            control.socks.send_msg(world, bob,
                "Now at: {}".format(bob.cur_loc))
        except:
            pass
    elif msg == curses.KEY_UP:
        control.socks.send_msg(world, bob, "handle_user_input... up")
    else:
        control.socks.send_msg(world, bob, "Huh?  {}".format(msg))
 
    return should_exit
