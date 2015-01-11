#!/usr/bin/python3.4

import model.tile
import control.move
import control.db
import control.uinput
import ui.mymap
import ui.ui
import curses
import ui.text

"""
This is a temporary function to help setup a world for me.
This makes a single tile and sets up it's uid and coord.
"""
def mtile(uid, coord):
    tile = model.tile.Tile()
    tile.uid = uid
    tile.coord = coord
    return tile
"""
This function initializes the different windows for the logged in user.
It also starts the main loop of the game.
TODO: The "logged" in user is statically assigned.  Need to actually
    let someone log in to the game.
"""
def main(stdscr):
    # attach the window screens to the logged in user
    player = entities[0]
    text_win, map_win, cmd_win = ui.ui.setup_windows(stdscr)
    player.map_win = map_win
    player.text_win = text_win
    player.cmd_win = cmd_win

    # display the world map
    ui.mymap.display_map(ui.ui.world, (0,0), 3, map_win)
    map_win.noutrefresh()

    # I think this is to make sure the numpad gets interpreted properly
    player.map_win.keypad(True)
    player.text_win.keypad(True)
    player.cmd_win.keypad(True)

    # Make userinput non-blocking (use nodelay(True)):
    # To make it wait some number of milliseconds, use timeout(ms)
    player.cmd_win.timeout(1000)
    player.map_win.timeout(100)
    player.text_win.timeout(100)

    # The following would be for centering control on the map window
    #ui.ui.handle_map_input(map_win, ui.ui.world, player)

    # We are going to center control of the game on the command window
    ui.text.add_msg(player, "Welcome to my game!")
    should_exit = False
    while not should_exit:
        user_input = ui.ui.handle_cmd_input(cmd_win, player)
        should_exit = control.uinput.handle_user_input(player, user_input)
    
    return True

if __name__ == "__main__":


    """
    entities = []
    # creates entity bob
    bob = model.tile.Entity()
    bob.name = "Bob"
    bob.symbol = "@"
    bob.cur_loc = (0, 0)
    bob.hp = 20
    bob.default_hp = 20
    entities.append(bob)
    #print("Name: {} Symbol: {}".format(bob.name, bob.symbol))

    # creates entity tim
    tim = model.tile.Entity()
    tim.name = "Tim"
    tim.symbol = "T"
    tim.cur_loc = (1, 0)
    tim.hp = 20
    tim.default_hp = 20
    entities.append(tim)
    #print("Name: {} Symbol: {}".format(tim.name, tim.symbol))

    # create the temporary world (it is a 4x4 world)
    dim = 3
    uuid = 0
    world = {}
    for y in range(-dim, dim+1):
        for x in range(-dim, dim+1):
            world[(x,y)] = mtile(uuid, (x,y))
            uuid = uuid+1
    ui.ui.world = world
    """

    #ui.ui.world = world

    #control.db.clean_tables()
    """
    control.db.drop_tables()
    print("Saving the world!")
    control.db.setup_tables()
    control.db.save_world(ui.ui.world)
    print("Done saving the world!")
    """

    #print("Now loading the world!")
    ui.ui.world = control.db.load_world()
    entities = control.db.load_entities()

    entities[0].cur_loc = (0, 0)
    entities[1].cur_loc = (1, 0)
    ui.ui.world[(0,0)].entities.append(entities[0])     #bob
    ui.ui.world[(1,0)].entities.append(entities[1])     #tim

    # need to attach curses windows to the player (bob)
    # I do this in the  main function

    curses.wrapper(main)

    """
    control.db.drop_tables()
    control.db.setup_tables()
    control.db.save_entities(entities)
    control.db.save_world(ui.ui.world)
    """

    #control.move.move(bob, world[(0,0)], world[(0,1)])

    #ui.mymap.display_map(world, (0,0), 3)
