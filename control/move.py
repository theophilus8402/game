#!/usr/bin/python3.4

def move(entity, cur_tile, dest_tile):
    print("Moving: {} From: {} To: {}".format(entity.symbol, cur_tile.uid,
        dest_tile.uid))
