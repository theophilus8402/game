#!/usr/bin/python3.4

import ui.text
import control.move
import curses

def handle_user_input(bob, msg):

    should_exit = False

    if msg == "exit":
        should_exit = True
    if msg == curses.KEY_UP:
        ui.text.add_msg(bob, "handle_user_input... up")
    else:
        ui.text.add_msg(bob, "Huh?  {}".format(msg))

    return should_exit


def handle_macro(bob, key):

    if key == "KEY_UP":
        x = bob.cur_loc_x
        y = bob.cur_loc_y
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
        x = bob.cur_loc_x
        y = bob.cur_loc_y
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
        x = bob.cur_loc_x
        y = bob.cur_loc_y
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
        x = bob.cur_loc_x
        y = bob.cur_loc_y
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
