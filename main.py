#!/usr/bin/python3.4

import model.tile
import control.move
import ui.map

def mtile(uid, coord):
    tile = model.tile.Tile()
    tile.uid = uid
    tile.x, tile.y = coord
    return tile

if __name__ == "__main__":

    world = model.tile.world

    bob = model.tile.Entity()
    bob.name = "Bob"
    bob.symbol = "@"
    print("Name: {} Symbol: {}".format(bob.name, bob.symbol))

    dim = 3
    uuid = 0
    for y in range(-dim, dim+1):
        for x in range(-dim, dim+1):
            world[(x,y)] = mtile(uuid, (x,y))
            uuid = uuid+1

    control.move.move(bob, world[(1,1)], world[(1,0)])

    ui.map.display_map(world, (0,0), 3)
