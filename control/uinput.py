#!/usr/bin/python3.4

import ui.text
import control.move
import control.roll
import curses
import re
import control.admin

re_hit = re.compile("hit (?P<who>\w+)")
re_make_tile = re.compile("make tile (?P<direction>\w+)")

def find_entity_in_tile(target_name, entities):
    the_entity = None
    for entity in entities:
        if target_name.lower() == entity.name.lower():
            the_entity = entity
            break
    return the_entity

def find_target_nearby(bob, target_name):
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
                ui.ui.world[(x+mod_x, y+mod_y)].entities)
            if target:
                break
        except:
            target = None
    return target

def handle_user_input(bob, msg):

    should_exit = False

    if msg == "exit":
        should_exit = True
    # the problem with the below is that we need to make the variable
    #   attached to individual not the game at large
    #elif control.admin.make_tile_handle:
        #control.admin.make_tile
    elif re_hit.match(msg):
        result = re_hit.match(msg)
        target_name = result.group("who")
        control.socks.send_msg(ui.ui.world, bob,
            "You want to hit {}?!".format(target_name))
        attack_roll = control.roll.roll(2, 6, 1)
        control.socks.send_msg(ui.ui.world, bob,
            "Attack roll: {}".format(attack_roll))
        dmg_roll = control.roll.roll(1, 6, 2)
        control.socks.send_msg(ui.ui.world, bob,
            "Dmg roll: {}".format(dmg_roll))

        # find the target nearby
        target_entity = find_target_nearby(bob, target_name)
        if target_entity:
            control.socks.send_msg(ui.ui.world, bob,
                "Found him at {}".format(target_entity.cur_loc))
            # apply dmg
            target_entity.hp = target_entity.hp - dmg_roll
            if target_entity.hp <= 0:
                control.socks.send_msg(bob, "You killed {}!".format(
                    target_name))
                ui.mymap.kill_creature(ui.ui.world, bob, target_entity)
        else:
            control.socks.send_msg(ui.ui.world, bob, "Couldn't find him...")
    elif re_make_tile.match(msg):
        result = re_make_tile.match(msg)
        direction = result.group("direction")
        control.admin.make_tile(bob, msg, direction)
    elif msg == curses.KEY_UP:
        control.socks.send_msg(ui.ui.world, bob, "handle_user_input... up")
    else:
        control.socks.send_msg(ui.ui.world, bob, "Huh?  {}".format(msg))

    return should_exit
