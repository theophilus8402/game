#!/usr/bin/python3.4

def display_map(world, bob, center=None, dimension=None):
    if center == None:
        center = bob.coord
    if dimension == None:
        dimension = bob.visual_range
    map_rows = []     # a list of the string for each row
    x, y = center
    """
    print("Center: {}".format(center))
    print("Top Left: {}  Top Right: {}".format((x-dimension,y+dimension),
        (x+dimension,y-dimension)))
    """
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
    bob.send_msg("\n".join(map_rows))
    return True


