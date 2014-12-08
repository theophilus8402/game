#!/usr/bin/python3.4

import model.tile
import control.move
import control.db
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
    player = bob
    text_win, map_win, cmd_win = ui.ui.setup_windows(stdscr)

    ui.mymap.display_map(ui.ui.world, (0,0), 3, map_win)

    map_win.noutrefresh()
    curses.doupdate()

    player.map_win = map_win
    player.text_win = text_win
    player.cmd_win = cmd_win

    ui.text.add_msg(player, "Hey, hey!")
    ui.ui.handle_map_input(map_win, ui.ui.world, player)
    map_win.getkey()
    return True

if __name__ == "__main__":

    world = {}

    bob = model.tile.Entity()
    bob.name = "Bob"
    bob.symbol = "@"
    #print("Name: {} Symbol: {}".format(bob.name, bob.symbol))

    tim = model.tile.Entity()
    tim.name = "Tim"
    tim.symbol = "T"
    #print("Name: {} Symbol: {}".format(tim.name, tim.symbol))

    """
    dim = 3
    uuid = 0
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

    ui.ui.world[(0,0)].entities.append(bob)
    ui.ui.world[(1,0)].entities.append(tim)

    curses.wrapper(main)

    #control.move.move(bob, world[(0,0)], world[(0,1)])

    #ui.mymap.display_map(world, (0,0), 3)
