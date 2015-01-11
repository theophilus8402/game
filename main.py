#!/usr/bin/python3.4

import model.tile
import control.move
import control.db
import control.uinput
import ui.mymap
import ui.ui
import curses
import ui.text

def mtile(uid, coord):
    tile = model.tile.Tile()
    tile.uid = uid
    tile.x, tile.y = coord
    return tile

def main(stdscr):
    player = entities[0]
    text_win, map_win, cmd_win = ui.ui.setup_windows(stdscr)

    ui.mymap.display_map(ui.ui.world, (0,0), 3, map_win)

    map_win.noutrefresh()
    curses.doupdate()

    player.map_win = map_win
    player.text_win = text_win
    player.cmd_win = cmd_win

    # I think this is to make sure the numpad gets interpreted properly
    player.map_win.keypad(True)
    player.text_win.keypad(True)
    player.cmd_win.keypad(True)

    # Make userinput non-blocking (use nodelay(True)):
    # To make it wait some number of milliseconds, use timeout(ms)
    player.cmd_win.timeout(1000)
    player.map_win.timeout(100)
    player.text_win.timeout(100)

    ui.text.add_msg(player, "Hey, hey!")
    #ui.ui.handle_map_input(map_win, ui.ui.world, player)
    should_exit = False
    while not should_exit:
        user_input = ui.ui.handle_cmd_input(cmd_win, player)
        should_exit = control.uinput.handle_user_input(player, user_input)
    
    #map_win.getkey()
    return True

if __name__ == "__main__":


    """
    entities = []
    bob = model.tile.Entity()
    bob.name = "Bob"
    bob.symbol = "@"
    bob.cur_loc_x = 0
    bob.cur_loc_y = 0
    bob.hp = 20
    bob.default_hp = 20
    entities.append(bob)
    #print("Name: {} Symbol: {}".format(bob.name, bob.symbol))

    tim = model.tile.Entity()
    tim.name = "Tim"
    tim.symbol = "T"
    tim.cur_loc_x = 1
    tim.cur_loc_y = 0
    tim.hp = 20
    tim.default_hp = 20
    entities.append(tim)
    #print("Name: {} Symbol: {}".format(tim.name, tim.symbol))

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

    entities[0].cur_loc_x = 0
    entities[0].cur_loc_y = 0
    entities[1].cur_loc_x = 1
    entities[1].cur_loc_y = 0
    ui.ui.world[(0,0)].entities.append(entities[0])     #bob
    ui.ui.world[(1,0)].entities.append(entities[1])     #tim

    curses.wrapper(main)

    """
    control.db.drop_tables()
    control.db.setup_tables()
    control.db.save_entities(entities)
    control.db.save_world(ui.ui.world)
    """

    #control.move.move(bob, world[(0,0)], world[(0,1)])

    #ui.mymap.display_map(world, (0,0), 3)
