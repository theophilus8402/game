#!/usr/bin/python3.4

from model.tile import get_symbol

def display_map(world, entity, center=None, dimension=None):
    #TODO: Figure out how to display a legend for the map
    if center == None:
        center = entity.coord
    if dimension == None:
        dimension = entity.visual_range
    map_rows = []     # a list of the string for each row
    x, y = center
    for j in range(-dimension, dimension+1).__reversed__():
        row = []
        for i in range(-dimension, dimension+1):
            coord = (x+i,y+j)
            try:
                row.append(get_symbol(world.tiles[coord]))
            except:
                # the a tile doesn't exist in the corresponding coord
                row.append(" ")
        # turn the row into a string and append it to the list
        if len(row) > 0: map_rows.append("".join(row))
    entity.comms.send("\n".join(map_rows))
    return True


