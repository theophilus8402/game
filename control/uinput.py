#!/usr/bin/python3.4

import control.move
import control.roll
import control.admin
import control.socks
import control.mymap
import control.entity
import model.msg
import re
from datetime import datetime, timedelta


re_hit = re.compile("hit (?P<who>\w+)")
re_make_tile = re.compile("make tile \(([-0-9]+), ([-0-9]+)\) ?(\d+x\d+)?")
re_cast_spell = re.compile("cast (.+) at (\w+)")

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
        bob.send_msg("Well, we'll miss you!  Goodbye!")
        control.socks.actually_send_msgs(world, bob)
        control.socks.remove_connection(world, bob.sock)
    elif bob.special_state:
        if bob.special_state == "login":
            control.socks.login(world, bob, msg)
    elif re_cast_spell.match(msg):
        #TODO: maybe change it so we pass the whole message to spell?
        #   that way we can let some complicated spells handle stuff

        # get names
        result = re_cast_spell.match(msg)
        spell_name = result.group(1)
        target_name = result.group(2)

        # verify info
        spell = None
        target = None
        try:
            spell = world.spells[spell_name]
        except:
            bob.send_msg("What spell is that???")
            pass
        try:
            target = world.find_entity(target_name)
        except:
            bob.send_msg("Who???")
            pass

        # cast the spell
        if spell and target:
            spell.cast(spell, world, bob, target)
        

    elif re_hit.match(msg):
        result = re_hit.match(msg)
        target_name = result.group("who")
        bob.send_msg("You want to hit {}?!".format(target_name))
        attack_roll = control.roll.roll(2, 6, 1)
        bob.send_msg("Attack roll: {}".format(attack_roll))
        dmg_roll = -control.roll.roll(1, 6, 2)
        bob.send_msg("Dmg roll: {}".format(dmg_roll))

        # find the target nearby
        target_entity = find_target_nearby(world, bob, target_name)
        if target_entity:
            bob.send_msg("Found him at {}".format(target_entity.cur_loc))
            # apply dmg
            target_entity.change_hp(bob, dmg_roll)
        else:
            bob.send_msg("Couldn't find him...")
    elif re_make_tile.match(msg):
        result = re_make_tile.match(msg)
        x = int(result.group(1))
        y = int(result.group(2))
        coord = (x, y)
        dimensions = result.group(3)
        #dimensions = None
        control.admin.make_tile(world, bob, coord, dimensions)
    # meditate
    elif msg == "meditate":
        td = timedelta(seconds=3)
        msg = model.msg.Msgs(bob, td, "meditate", True)
        world.add_msg(msg)
        bob.add_status("meditating")
    elif msg == "n":
        x, y = bob.cur_loc
        try:
            control.move.move(world, bob, (x,y), (x,y+1))
            control.mymap.display_map(world, bob)
            bob.send_msg("Now at: {}".format(bob.cur_loc))
            # need this at the end, if it fails, the try block is gonna stop
            bob.remove_status("meditating")
        except:
            pass
    elif msg == "e":
        x, y = bob.cur_loc
        try:
            control.move.move(world, bob, (x,y), (x+1,y))
            control.mymap.display_map(world, bob)
            bob.send_msg("Now at: {}".format(bob.cur_loc))
            bob.remove_status("meditating")
        except:
            pass
    elif msg == "s":
        x, y = bob.cur_loc
        try:
            control.move.move(world, bob, (x,y), (x,y-1))
            control.mymap.display_map(world, bob)
            bob.send_msg("Now at: {}".format(bob.cur_loc))
            bob.remove_status("meditating")
        except:
            pass
    elif msg == "w":
        x, y = bob.cur_loc
        try:
            control.move.move(world, bob, (x,y), (x-1,y))
            control.mymap.display_map(world, bob)
            bob.send_msg("Now at: {}".format(bob.cur_loc))
            bob.remove_status("meditating")
        except:
            pass
    else:
        bob.send_msg("Huh?  {}".format(msg))
 
    return should_exit
