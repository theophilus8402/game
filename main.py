#!/usr/bin/python3.4

import model.tile
import control.move
import control.db
import control.uinput
import ui.mymap
import ui.ui
import curses
import ui.text

"""
This is a temporary function to help setup a world for me.
This makes a single tile and sets up it's uid and coord.
"""
def mtile(uid, coord):
    tile = model.tile.Tile()
    tile.uid = uid
    tile.coord = coord
    return tile


def create_temp_world():
    # create the temporary world (it is a 4x4 world)
    dim = 3
    uuid = 0
    world = {}
    for y in range(-dim, dim+1):
        for x in range(-dim, dim+1):
            world[(x,y)] = mtile(uuid, (x,y))
            uuid = uuid+1
    return world


def create_temp_guy(name, sym, coord, hp, def_hp):
    # creates entity bob
    bob = model.tile.Entity()
    bob.name = name
    bob.symbol = sym
    bob.cur_loc = coord
    bob.hp = hp
    bob.default_hp = def_hp
    return bob


if __name__ == "__main__":

    """
    # Create the temp world:
    ui.ui.world = create_temp_world()
    bob = create_temp_guy("Bob", "@", (0, 0), 20, 20)
    tim = create_temp_guy("Tim", "T", (1, 0), 20, 20)
    entities = [bob, tim]
    ui.ui.world[(0,0)].entities.append(bob)
    ui.ui.world[(1,0)].entities.append(tim)
    """

    """
    empty the tables:
    control.db.clean_tables()

    # add the temp guys
    control.db.add_entity(bob)
    control.db.add_entity(tim)
    """

    """
    Now loading the world!
    """
    ui.ui.world = control.db.load_world()
    entities = control.db.load_entities(ui.ui.world)

    """
    give em bob as the player:
    """
    bob = entities[0]

    # enter main loop of the game

    control.db.save_entities(entities)
    control.db.save_world(ui.ui.world)

    """
    control.db.drop_tables()
    control.db.setup_tables()
    """
