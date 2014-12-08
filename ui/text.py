#!/usr/bin/python3.4

import curses

def add_msg(bob, msg):
    bob.messages.append(msg)
    #bob.text_win.
    display_msgs(bob)

def display_msgs(bob):
    # figure out window height
    max_y, max_x = bob.text_win.getmaxyx()

    # figure out starting place in messages list
    i = bob.msg_start

    # go through each msg figuring out how wide it needs to be

    # determine how much to print
    range_y = min(max_y, len(bob.messages))

    # print msgs
    bob.text_win.clear()
    for m in range(range_y):
        bob.text_win.addstr(m, 0, bob.messages[i+m])
    bob.text_win.noutrefresh()
    curses.doupdate()
