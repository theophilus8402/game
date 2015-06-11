#!/usr/bin/python3.4

import control.socks

"""
We are assuming the entity can move (i.e. not paralyzed, there is nothing
blocking it...
"""
def move(world, entity, cur_loc, dst_loc):
    cur_tile = world.tiles[cur_loc]
    dst_tile = world.tiles[dst_loc]

    # make sure entity is in cur_tile
    if entity in cur_tile.entities:
        print("{} -> {}".format(cur_loc, dst_loc))

        # remove entity from cur_tile
        cur_tile.entities.remove(entity)

        # add entity to dest_tile
        dst_tile.entities.append(entity)
        entity.cur_loc = dst_tile.coord

    return (world, entity)
