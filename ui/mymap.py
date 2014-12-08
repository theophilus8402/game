#!/usr/bin/python3.4

"""
map_win is a curses window
"""
def display_map(world, center, dimension, map_win):
    x, y = center
    n = 1   # keeps track of where we are on the map screen
    for j in range(-dimension, dimension+1).__reversed__():
        row = []
        for i in range(-dimension, dimension+1):
            coord = (x+i,y+j)
            if world.__contains__(coord):
                """
                ents = []
                for ent in world[coord].entities:
                    ents.append(ent.name)
                print("{}: {}".format(coord, ents))
                """
                row.append(world[coord].get_symbol())
        #if len(row) > 0: print("".join(row))
        if len(row) > 0: map_win.addstr(n, 1, "".join(row))
        n = n+1
