#!/usr/bin/python3.4

import curses
import curses.ascii
import math

def handle_cmd_input(win):
    user_str = []

    while True:
        key = win.getkey()
        if curses.ascii.isalnum(key):
            user_str.append(key)
            win.addstr(key)
            win.noutrefresh()
            curses.doupdate()
        elif ord(key) == 0x09:      # tab
            break
        elif ord(key) == 0x7f:      # backspace
            break
        elif ord(key) == 0x0a:      # carriage return
            break
        elif ord(key) == 0x20:      # space
            break
        elif ord(key) == 0x1b:      # ESC
            break
        """
        else:
            win.addstr(key)
            win.noutrefresh()
            curses.doupdate()
            break
        """
    return "".join(user_str)


def main(stdscr):
    # Clear the screen
    stdscr.clear()


    # Determine Text Window
    # Width 60% of window
    text_width = math.ceil(curses.COLS*.6)
    text_height = curses.LINES-2
    text_win = curses.newwin(text_height, text_width, 0, 0)

    # Determine Map Window
    # Width is the rest
    map_width = curses.COLS-text_width+1
    map_start_x = text_width-1
    map_height = text_height
    map_win = curses.newwin(map_height, map_width, 0, map_start_x)

    # Determine Command Border window
    cmd_brdr_width = curses.COLS
    cmd_brdr_height = 3
    cmd_brdr_start_x = 0
    cmd_brdr_start_y = curses.LINES-3
    cmd_brdr_win = curses.newwin(cmd_brdr_height, cmd_brdr_width, cmd_brdr_start_y, cmd_brdr_start_x)

    # Determine Command Line Window
    cmd_width = curses.COLS-2
    cmd_height = 1
    cmd_start_x = 1
    cmd_start_y = curses.LINES-2
    cmd_win = curses.newwin(cmd_height, cmd_width, cmd_start_y, cmd_start_x)

    # Draw borders
    text_win.border()
    text_win.noutrefresh()
    cmd_brdr_win.border(curses.ACS_VLINE,curses.ACS_VLINE,curses.ACS_HLINE,curses.ACS_HLINE,curses.ACS_LTEE,)
    cmd_brdr_win.noutrefresh()
    map_win.border(curses.ACS_VLINE,curses.ACS_VLINE,curses.ACS_HLINE,curses.ACS_HLINE,curses.ACS_TTEE,curses.ACS_URCORNER,curses.ACS_BTEE,curses.ACS_RTEE)
    map_win.noutrefresh()

    curses.doupdate()
    cmd_win.getkey()

    # Add stuff
    map_win.addstr(2,2,"Map!")
    map_win.noutrefresh()
    curses.doupdate()
    #cmd_win.getkey()

    text_win.addstr(1,1,"Hello!")
    text_win.noutrefresh()
    curses.doupdate()
    #cmd_win.getkey()

    user_str = handle_cmd_input(cmd_win)
    text_win.addstr(2,1,user_str)
    text_win.noutrefresh()
    curses.doupdate()
    cmd_win.getkey()

    '''
    cmd_win.addstr("Yarr!")
    cmd_win.noutrefresh()
    curses.doupdate()
    '''


if __name__ == "__main__":
    curses.wrapper(main)
