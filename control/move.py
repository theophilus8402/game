#!/usr/bin/python3.4

"""
We are assuming the entity can move (i.e. not paralyzed, there is nothing
blocking it...
"""
def move(entity, cur_tile, dest_tile):
    # make sure entity is in cur_tile
    if entity not in cur_tile.entities:
        return False

    # remove entity from cur_tile
    cur_tile.entities.remove(entity)

    # add entity to dest_tile
    dest_tile.entities.append(entity)
    entity.cur_loc = dest_tile.coord
