#!/usr/bin/python3.4

import curses
import control.socks

"""
map_win is a curses window
"""
def display_map(world, center, dimension, bob):
    map_rows = []     # a list of the string for each row
    x, y = center
    n = 1   # keeps track of where we are on the map screen
    for j in range(-dimension, dimension+1).__reversed__():
        row = []
        for i in range(-dimension, dimension+1):
            coord = (x+i,y+j)
            try:
                """
                # this will be used in the future to have a legend of
                #   all the creatures on the map
                ents = []
                for ent in world.tiles[coord].entities:
                    ents.append(ent.name)
                """
                row.append(world.tiles[coord].get_symbol())
            except:
                # the a tile doesn't exist in the corresponding coord
                row.append(" ")
        # turn the row into a string and append it to the list
        if len(row) > 0: map_rows.append("".join(row))
        n = n+1
    control.socks.send_msg(world, bob, "\n".join(map_rows))
    return True


def kill_creature(world, killer, dead_guy):
    # remove creature from the map
    world.tiles[dead_guy.cur_loc].entities.remove(dead_guy)
    #TODO: need to figure out how to remove the dead_guy's cur_loc

    # update map window
    display_map(world, (0, 0), 3, killer)
    return True
