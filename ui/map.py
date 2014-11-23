#!/usr/bin/python3.4

def display_map(world, center, dimension):
    x, y = center
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
        if len(row) > 0: print("".join(row))
