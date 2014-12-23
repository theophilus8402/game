#!/usr/bin/python3.4

import curses

def add_msg(bob, msg):
    bob.messages.append(msg)

    start = bob.disp_msg_start

    scroll = bob.text_scroll

    # determine if we need to break msg up on multiple lines
    # the full length msgs gets stored on one line in messages
    # this is for display purposes
    height, width = bob.text_win.getmaxyx()
    while len(msg) > width:
        front_part = msg[0:width]
        msg = msg[width:]
        bob.disp_msgs.append(front_part)
        if scroll and (len(bob.disp_msgs[start:]) > height):
            start = start+1
    bob.disp_msgs.append(msg)
    if scroll and (len(bob.disp_msgs[start:]) > height):
        start = start+1
    bob.disp_msg_start = start
    display_msgs(bob)

def display_msgs(bob):
    # figure out window height
    max_y, max_x = bob.text_win.getmaxyx()

    # figure out starting place in messages list
    start = bob.disp_msg_start

    # go through each msg figuring out how wide it needs to be

    # determine how much to print
    range_y = min(max_y, len(bob.disp_msgs))

    # print msgs
    bob.text_win.clear()
    for m in range(range_y):
        bob.text_win.addstr(m, 0, bob.disp_msgs[start+m])
    bob.text_win.noutrefresh()
    curses.doupdate()
