#!/usr/bin/python3.4

import ui.text
import control.move
import control.roll
import curses
import re

re_hit = re.compile("hit (?P<who>\w+)")

def find_entity_in_tile(target_name, entities):
    for entity in entities:
        if target_name.lower() == entity.name.lower():
            return entity

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
    elif re_hit.match(msg):
        result = re_hit.match(msg)
        target_name = result.group("who")
        ui.text.add_msg(bob, "You want to hit {}?!".format(target_name))
        attack_roll = control.roll.roll(2, 6, 1)
        ui.text.add_msg(bob, "Attack roll: {}".format(attack_roll))
        dmg_roll = control.roll.roll(1, 6, 2)
        ui.text.add_msg(bob, "Dmg roll: {}".format(dmg_roll))

        # find the target nearby
        target_entity = find_target_nearby(bob, target_name)
        if target_entity:
            ui.text.add_msg(bob, "Found him at {}".format(
                target_entity.cur_loc))
            # apply dmg
            target_entity.hp = target_entity.hp - dmg_roll
            if target_entity.hp <= 0:
                ui.text.add_msg(bob, "You killed {}!".format(target_name))
                ui.mymap.kill_creature(ui.ui.world, bob, target_entity)
        else:
            ui.text.add_msg(bob, "Couldn't find him...")
        
    elif msg == curses.KEY_UP:
        ui.text.add_msg(bob, "handle_user_input... up")
    else:
        ui.text.add_msg(bob, "Huh?  {}".format(msg))

    return should_exit


def handle_macro(bob, key):

    if key == "KEY_UP":
        x, y = bob.cur_loc
        world = ui.ui.world
        try:
            control.move.move(bob, world[(x,y)], world[(x,y+1)])
            ui.mymap.display_map(world, (0,0), 3, bob.map_win)
            ui.text.add_msg(bob, "Up arrow!")
            bob.map_win.noutrefresh()
            curses.doupdate()
        except:
            pass
    elif key == "KEY_LEFT":
        x, y = bob.cur_loc
        world = ui.ui.world
        try:
            control.move.move(bob, world[(x,y)], world[(x-1,y)])
            ui.mymap.display_map(world, (0,0), 3, bob.map_win)
            ui.text.add_msg(bob, "Left arrow!")
            bob.map_win.noutrefresh()
            curses.doupdate()
        except:
            pass
    elif key == "KEY_RIGHT":
        x, y = bob.cur_loc
        world = ui.ui.world
        try:
            control.move.move(bob, world[(x,y)], world[(x+1,y)])
            ui.mymap.display_map(world, (0,0), 3, bob.map_win)
            ui.text.add_msg(bob, "Right arrow!")
            bob.map_win.noutrefresh()
            curses.doupdate()
        except:
            pass
    elif key == "KEY_DOWN":
        x, y = bob.cur_loc
        world = ui.ui.world
        try:
            control.move.move(bob, world[(x,y)], world[(x,y-1)])
            ui.mymap.display_map(world, (0,0), 3, bob.map_win)
            ui.text.add_msg(bob, "Down arrow!")
            bob.map_win.noutrefresh()
            curses.doupdate()
        except:
            pass
    else:
        ui.text.add_msg(bob, "macro... err...")
