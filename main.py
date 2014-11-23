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

    world = {}

    bob = model.tile.Entity()
    bob.name = "Bob"
    bob.symbol = "@"
    print("Name: {} Symbol: {}".format(bob.name, bob.symbol))

    tim = model.tile.Entity()
    tim.name = "Tim"
    tim.symbol = "T"
    print("Name: {} Symbol: {}".format(tim.name, tim.symbol))

    dim = 3
    uuid = 0
    for y in range(-dim, dim+1):
        for x in range(-dim, dim+1):
            world[(x,y)] = mtile(uuid, (x,y))
            uuid = uuid+1

    world[(0,0)].entities.append(bob)
    world[(1,0)].entities.append(tim)

    control.move.move(bob, world[(0,0)], world[(0,1)])

    ui.map.display_map(world, (0,0), 3)

