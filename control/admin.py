#!/usr/bin/python3.4

import control.socks
import model.tile
import re

"""
For now, I'm just going to copy the tile I'm on to the given coord.

expecting dimensions to be a string that looks like this: "5x3"
If given dimensions, the start of the area created will be at the top left
    starting at the coord given.

In the future, I'll take a series of coords on the same line and copy
the cur_loc info to all of the coords.

I'll also need to make a function to modify the tiles.
"""
def make_tile(world, bob, start_coord, dimensions=None):
    coords = []

    if dimensions:
        dim_x, dim_y = dimensions.split("x")
        dim_x = int(dim_x)
        dim_y = int(dim_y)

        coord_x, coord_y = start_coord
        for cx in range(dim_x):
            for cy in range(dim_y):
                new_coord = (coord_x+cx, coord_y-cy)
                coords.append(new_coord)
    else:
        coords.append(start_coord)

    # make all the tiles
    for coord in coords:
        bob.send_msg("You want to add a tile at loc: {}?".format(coord))

        # make sure a tile doesn't exist at the given coord
        if coord in world.tiles.keys():
            bob.send_msg("That tile already exists!")
        else:
            src_tile = world.tiles[bob.cur_loc]

            # create the tile(s)
            new_tile = model.tile.Tile()
            new_tile.uid = world.get_new_tile_uid()
            new_tile.ground = src_tile.ground
            new_tile.coord = coord
            new_tile.default_symbol = src_tile.default_symbol
            bob.send_msg("Creating the following tile:")
            bob.send_msg("uid: {} ground: {} coord: {} default_symbol: {}"
                .format(new_tile.uid, new_tile.ground, new_tile.coord,
                    new_tile.default_symbol))

            # add them to the world
            world.tiles[coord] = new_tile
            # redraw the world
            control.mymap.display_map(world, bob)
    return world


"""
def make_tile_handle(bob, msg):
    # got through a default set of questions... hrm... how do I do this?
        # solving this ties in with handling quests
    if make_tile_handle_symbol:
        # TODO: check for appropriate symbol

        symbol = msg
        make_tile_handle_symbol = False
"""
