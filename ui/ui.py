#!/usr/bin/python3.4

import ui.mymap
import ui.text
import control.move
import control.uinput
import curses.ascii
import math
import sys
import traceback

world = {}

def handle_map_input(win, world, entity):
    while True:
        key = win.getkey()
        if key == "h":
            # determine current coords
            x, y = entity.cur_loc
            # move west
            try:
                control.move.move(entity, world[(x,y)], world[(x-1,y)])
                ui.mymap.display_map(world, (0,0), 3, win)
                ui.text.add_msg(entity, "Moved west.")
            except:
                pass
        elif key == "j":
            # determine current coords
            x, y = entity.cur_loc
            # move south
            try:
                control.move.move(entity, world[(x,y)], world[(x,y-1)])
                ui.mymap.display_map(world, (0,0), 3, win)
                ui.text.add_msg(entity, "Moved south.")
            except:
                pass
        elif key == "k":
            # determine current coords
            x, y = entity.cur_loc
            # move north
            try:
                control.move.move(entity, world[(x,y)], world[(x,y+1)])
                ui.mymap.display_map(world, (0,0), 3, win)
                ui.text.add_msg(entity, "Moved north.")
            except:
                pass
        elif key == "l":
            # determine current coords
            x, y = entity.cur_loc
            # move east
            try:
                control.move.move(entity, world[(x,y)], world[(x+1,y)])
                ui.mymap.display_map(world, (0,0), 3, win)
                ui.text.add_msg(entity, "Moved east.")
            except:
                pass
        else:
            ui.text.add_msg(entity, "Something else.")
            break
        win.noutrefresh()
        curses.doupdate()
    return True
        

def handle_cmd_input(win, entity):
    user_str = []

    """
    curses.echo()
    user_str = win.getstr()
    curses.noecho()
    return user_str
    """
    while True:
        str_index = 0
        try:
            key = win.getkey()
        except KeyboardInterrupt:
            #key = None
            ui.text.add_msg(entity, "handle_cmd_input key: key int: {}".format(traceback.print_tb(sys.exc_info()[2])))
            break
        except:
            #ui.text.add_msg(entity, "exception")
            ui.text.add_msg(entity, "key problem!")
            key = None
        #ui.text.add_msg(entity, "handle_cmd_input key: {}".format(key))
        #control.uinput.handle_macro(entity, key)
        y, index = win.getyx()
        if key is None:
            pass
        #elif len(key) > 1:
            #control.uinput.handle_macro(entity, key)
            #ui.text.add_msg(entity, "handle_cmd_input key: len>1 {}".format(key))
        elif len(key) is 1 and curses.ascii.isprint(key):
            # add the ch based on where the cursor is
            user_str.insert(index, key)
            try:
                win.insch(key)
                win.move(y, index+1)
                str_index = str_index + 1
            except:
                # got to the end of the line
                # draw the end of the user_str closest to the cursor's end
                y, win_width = win.getmaxyx()
                win.clear()
                # NOTE! This is not correct... what if the string spills out over both ends?!
                if index <= (win_width/2):
                    # draw the beginning of the user_str
                    win.addstr(0,0,"".join(user_str[:win_width]))
                    win.move(y, index+1)
                else:
                    # draw the end of the user_str
                    win.addstr(0,0,"".join(user_str[-win_width+1:]))
                str_index = str_index + 1
                win.noutrefresh()
                curses.doupdate()
            ui.text.add_msg(entity, "handle_cmd_input key: print: {}".format(key))
        elif key == "KEY_BACKSPACE":      # backspace  if getch... ox7f
            # remove character (based on where the cursor is) from user_str
            if index > 0:
                user_str.pop(index-1)
                win.clear()
                # move cursor back one
                win.move(y, index-1)
                # redraw the line
                win.addstr(0,0,"".join(user_str))
                win.noutrefresh()
                curses.doupdate()
        elif key == "\n":      # carriage return  if getch... 0x0a
            # clear the line
            #ui.text.add_msg(entity, "handle_cmd_input key: carriage return")
            win.clear()
            break
        else:
            ui.text.add_msg(entity, "handle_cmd_input key: else... {}".format(key))
            control.uinput.handle_macro(entity, key)
        """
        elif ord(key) == 0x1b:      # ESC
            break
        elif ord(key) == 0x09:      # tab
            # dunno what to do here yet... I don't think I want to actually tab
            # I can use it to tab complete?
            pass
        """
        # ctrl-f
            # move the cursor forward one space
        # ctrl-b
            # move the cursor back one space
        # alt-f
            # move the cursor forward one word
        # alt-b
            # move the cursor back one word
        # ctrl-d
            # delete the ch where the cursor is
            # move what's to the right over to the left
            # remove the ch from user_str
            # don't move the cursor
        # alt-d
            # delete from the cursor to the next space (i.e. word)
        # ctrl-a
            # move the cursor to the beginning of the line
        # ctrl-e
            # move the cursor to the end of the line
        """
        elif ord(key) == 0x20:      # space
            # add the space based on where the cursor is
            user_str.insert(index, " ")
            # draw that space
            win.insch(" ")
            win.move(y, index+1)
        """
        #else:
            #win.addstr(key)
            #win.noutrefresh()
            #curses.doupdate()
            #break
    return "".join(user_str)


def setup_windows(stdscr):
    # Clear the screen
    stdscr.clear()

    """
    We are going to draw the borders on the main screen.
    So, we need to shrink all the other windows by one on each side.
    """

    # Determine Text Window
    # Width 60% of window
    text_width = math.ceil(curses.COLS*.6) - 2
    text_height = curses.LINES-4
    text_win = curses.newwin(text_height, text_width, 1, 1)

    # Determine Map Window
    # Width is the rest
    map_width = curses.COLS-text_width-1
    map_start_x = text_width
    map_height = text_height
    map_win = curses.newwin(map_height, map_width, 1, map_start_x)

    """
    # Determine Command Border window
    cmd_brdr_width = curses.COLS
    cmd_brdr_height = 3
    cmd_brdr_start_x = 0
    cmd_brdr_start_y = curses.LINES-3
    cmd_brdr_win = curses.newwin(cmd_brdr_height, cmd_brdr_width, cmd_brdr_start_y, cmd_brdr_start_x)
    """

    # Determine Command Line Window
    cmd_width = curses.COLS-2
    cmd_height = 1
    cmd_start_x = 1
    cmd_start_y = curses.LINES-2
    cmd_win = curses.newwin(cmd_height, cmd_width, cmd_start_y, cmd_start_x)

    # Draw borders
    """
    text_win.border()
    text_win.noutrefresh()
    cmd_brdr_win.border(curses.ACS_VLINE,curses.ACS_VLINE,curses.ACS_HLINE,curses.ACS_HLINE,curses.ACS_LTEE,)
    cmd_brdr_win.noutrefresh()
    map_win.border(curses.ACS_VLINE,curses.ACS_VLINE,curses.ACS_HLINE,curses.ACS_HLINE,curses.ACS_TTEE,curses.ACS_URCORNER,curses.ACS_BTEE,curses.ACS_RTEE)
    map_win.noutrefresh()
    """
    # draw top command window border
    #stdscr.addstr("".join(line))
    stdscr.border()
    """
    for i in range(cmd_width):
        stdscr.addch(cmd_start_y-1, 5, curses.ACS_HLINE)
    """
    stdscr.hline(cmd_start_y-1, 1, curses.ACS_HLINE, cmd_width)
    stdscr.noutrefresh()
    curses.doupdate()
    stdscr.addch(cmd_start_y-1, 1, curses.ACS_LTEE)
    #stdscr.addch(cmd_start_y-1, 0, curses.ACS_LTEE)
    stdscr.noutrefresh()
    curses.doupdate()
    #cmd_win.getkey()

    # Add stuff
    #text_win.addstr(1,1,"Hello!")
    #text_win.noutrefresh()

    #ui.mymap.display_map(world, (0,0), 3, map_win)
    # move the cursor to the middle of the map screen
    center_x = math.floor(map_width/2)
    center_y = math.floor(map_height/2)
    map_win.move(center_y, center_x)
    #map_win.addstr(2,2,"Map!")
    map_win.noutrefresh()
    curses.doupdate()
    #cmd_win.getkey()

    #curses.doupdate()
    #cmd_win.getkey()

    """
    user_str = handle_cmd_input(cmd_win)
    text_win.addstr(2,1,user_str)
    text_win.noutrefresh()
    curses.doupdate()
    cmd_win.getkey()
    """

    #handle_map_input(map_win)
    #map_win.getkey()

    '''
    cmd_win.addstr("Yarr!")
    cmd_win.noutrefresh()
    curses.doupdate()
    '''

    #return True
    return (text_win, map_win, cmd_win)


if __name__ == "__main__":
    import curses
    text_win, map_win, cmd_win = curses.wrapper(setup_windows)
