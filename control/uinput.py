#!/usr/bin/python3.4

import ui.text
import curses

def handle_user_input(bob, msg):

    should_exit = False

    if msg == "exit":
        should_exit = True
    if msg == curses.KEY_UP:
        ui.text.add_msg(bob, "handle_user_input... up")
    else:
        ui.text.add_msg(bob, "Huh?")

    return should_exit


def handle_macro(bob, key):

    if key == curses.KEY_UP:
        ui.text.add_msg(bob, "Up arrow!")
    else:
        ui.text.add_msg(bob, "macro... err...")
