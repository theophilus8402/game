#!/usr/bin/python3.4

import curses
import curses.ascii
import math

def handle_cmd_input(win):
    user_str = []

    """
    curses.echo()
    user_str = win.getstr()
    curses.noecho()
    return user_str
    """
    while True:
        str_index = 0
        key = win.getkey()
        y, index = win.getyx()
        if curses.ascii.isprint(key):
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
        elif ord(key) == 0x7f:      # backspace
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
        elif ord(key) == 0x0a:      # carriage return
            # clear the line
            win.clear()
            break
        elif ord(key) == 0x1b:      # ESC
            break
        elif ord(key) == 0x09:      # tab
            # dunno what to do here yet... I don't think I want to actually tab
            # I can use it to tab complete?
            pass
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
