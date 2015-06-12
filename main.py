#!/usr/bin/python3.4

import model.tile
import model.msgs
import control.spells
import control.move
import control.sqldb
import control.db
import control.uinput
import control.socks
import control.admin
import control.mymap
import curses

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
    world = model.tile.World()
    for y in range(-dim, dim+1):
        for x in range(-dim, dim+1):
            world.tiles[(x,y)] = mtile(uuid, (x,y))
            uuid = uuid+1
    return world


def create_temp_guy(name, sym, coord, hp, max_hp):
    # creates entity bob
    bob = model.tile.Entity()
    bob.name = name
    bob.symbol = sym
    bob.cur_loc = coord
    bob.cur_hp = hp
    bob.max_hp = max_hp
    return bob


if __name__ == "__main__":

    """
    # Create the temp world:
    world = create_temp_world()
    bob = create_temp_guy("Bob", "@", (0, 0), 20, 20)
    tim = create_temp_guy("Tim", "T", (1, 0), 20, 20)
    entities = [bob, tim]
    world.tiles[(0,0)].entities.append(bob)
    world.tiles[(1,0)].entities.append(tim)
    """

    """
    #SQL stuff
    world = control.sqldb.load_world()
    world.entities = control.sqldb.load_entities(world)
    control.sqldb.rebuild_entities_table(world.entities)
    empty the tables:
    control.db.clean_tables()

    # add the temp guys
    control.db.add_entity(bob)
    control.db.add_entity(tim)

    control.sqldb.save_world(world)
    control.db.drop_tables()
    control.db.setup_tables()
    """

    """
    Now loading the world!
    """
    world = model.tile.World()
    world.tiles, world.max_tile_uid = control.db.load_tiles("tiles.txt")
    world.entities = control.db.load_entities("entities.txt")
    # TODO: I should figure out a better way to set the dead room
    world.dead_room = world.tiles[(5, 3)]
    # put the entities on the map
    for entity_name in world.entities.keys():
        entity = world.entities[entity_name]
        world.tiles[entity.cur_loc].entities.append(entity)

    passwds = {}
    passwds["bob"] = "bob123"
    passwds["tim"] = "tim123"
    world.passwds = passwds

    # initialize spells
    simple_spells = control.db.load_spells("spells.txt")
    world.spells = control.spells.initialize_spells(simple_spells)

    #FOR TESTING
    bob = world.entities["bob"]
    tim = world.entities["tim"]
    bob.special_state = None
    from datetime import datetime, timedelta
    td = timedelta(seconds=3.5)
    msg = model.msgs.Msgs(bob, td, "meditate", True)
    import time
    n = 0
    bob.status_msgs.append("meditating")
    while True:
        time.sleep(1)
        if msg.check():
            recurring = msg.execute()
            if recurring:
                continue
            else:
                break
        n+=1
        if n>20:
            bob.status_msgs.remove("meditating")

    # enter main loop of the game
    #control.socks.server_loop(world)

    control.db.save_entities(world.entities, "entities.txt")
    control.db.save_tiles(world.tiles, "tiles2.txt")

    """
    # commands I've tested:
    #res_spell = world.spells["resurrection"]
    #res_spell.cast(res_spell, world, bob, tim)
    #control.uinput.handle_user_input(world, bob, "cast heal at tim")
    #control.entities.cast_spell(world, world.entities[0], world.entities[1], "resurrection")
    #control.admin.make_tile(world, world.entities[0], (3, 0), "2x1")
    #control.mymap.display_map(world, world.entities[0])
    """
