#!/usr/bin/python3.4

import control.socks

"""
We are assuming the entity can move (i.e. not paralyzed, there is nothing
blocking it...
"""
def move(world, entity, cur_loc, dst_loc):
    cur_tile = world.tiles[cur_loc]
    dst_tile = world.tiles[dst_loc]
    print("cur_loc: {} addr: {}".format(cur_loc, cur_tile))
    print("dst_loc: {} addr: {}".format(dst_loc, dst_tile))
    print(entity)

    """
    control.socks.send_msg(world, entity, "ent's cur loc: {}".format(
        entity.cur_loc))
    """

    # make sure entity is in cur_tile
    if entity in cur_tile.entities:

        # remove entity from cur_tile
        #cur_tile.entities.remove(entity)
        world.tiles[cur_loc].entities.remove(entity)

        # add entity to dest_tile
        #dst_tile.entities.append(entity)
        #entity.cur_loc = dest_tile.coord
        world.tiles[dst_loc].entities.append(entity)
        entity.cur_loc = world.tiles[dst_loc].coord
    """
    control.socks.send_msg(world, entity, "ent's cur loc: {}".format(
        entity.cur_loc))
    """
    return (world, entity)
