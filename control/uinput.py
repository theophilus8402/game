#!/usr/bin/python3.4

import control.move
import control.roll
import control.admin
import control.socks
import ui.mymap
import curses
import re

re_hit = re.compile("hit (?P<who>\w+)")
re_make_tile = re.compile("make tile (?P<direction>\w+)")

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
    # the problem with the below is that we need to make the variable
    #   attached to individual not the game at large
    #elif control.admin.make_tile_handle:
        #control.admin.make_tile
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
            target_entity.hp = target_entity.hp - dmg_roll
            if target_entity.hp <= 0:
                control.socks.send_msg(world, bob, "You killed {}!".format(
                    target_name))
                ui.mymap.kill_creature(world, bob, target_entity)
        else:
            control.socks.send_msg(world, bob, "Couldn't find him...")
    elif msg == "n":
        x, y = bob.cur_loc
        print(bob)
        try:
            control.socks.send_msg(world, bob,
                "cur loc: {}".format(bob.cur_loc))
            control.move.move(world, bob, (x,y), (x,y+1))
            ui.mymap.display_map(world, (0,0), 3, bob)
            control.socks.send_msg(world, bob, "Moving north!")
            control.socks.send_msg(world, bob,
                "cur loc: {}".format(bob.cur_loc))
        except:
            pass
    elif msg == "e":
        x, y = bob.cur_loc
        try:
            control.move.move(world, bob, (x,y), (x+1,y))
            ui.mymap.display_map(world, (0,0), 3, bob)
            control.socks.send_msg(world, bob, "moving east!")
        except:
            pass
    elif msg == "s":
        x, y = bob.cur_loc
        try:
            control.move.move(world, bob, (x,y), (x,y-1))
            ui.mymap.display_map(world, (0,0), 3, bob)
            control.socks.send_msg(world, bob, "moving south!")
        except:
            pass
    elif msg == "w":
        x, y = bob.cur_loc
        try:
            control.move.move(world, bob, (x,y), (x-1,y))
            ui.mymap.display_map(world, (0,0), 3, bob)
            control.socks.send_msg(world, bob, "moving west!")
        except:
            pass
    elif msg == curses.KEY_UP:
        control.socks.send_msg(world, bob, "handle_user_input... up")
    else:
        control.socks.send_msg(world, bob, "Huh?  {}".format(msg))
    """
    elif re_make_tile.match(msg):
        result = re_make_tile.match(msg)
        direction = result.group("direction")
        control.admin.make_tile(bob, msg, direction)
    """
 
    return should_exit
