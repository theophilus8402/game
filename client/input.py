def handle_macro(bob, key):

    if key == "KEY_UP":
        x, y = bob.cur_loc
        world = ui.ui.world
        try:
            control.move.move(bob, world[(x,y)], world[(x,y+1)])
            ui.mymap.display_map(world, (0,0), 3, bob.map_win)
            control.socks.send_msg(bob, "Up arrow!")
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
