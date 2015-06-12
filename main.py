#!/usr/bin/python3.4

import model.tile
import model.msgs
import control.spells
import control.move
import control.sqldb
import control.db.spell
import control.db.entity
import control.db.tile
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


def map_entities(world, entities):
    for entity_name in entities.keys():
        entity = entities[entity_name]
        world.tiles[entity.cur_loc].entities.append(entity)


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
    Now loading the world!
    """
    world = model.tile.World()
    world.tiles, world.max_tile_uid = control.db.tile.load_tiles("tiles.txt")
    world.basic_ents = control.db.entity.load_entities("basic_ents.txt")
    world.weapon_ents = control.db.entity.load_entities("weapon_ents.txt")
    world.armour_ents = control.db.entity.load_entities("armour_ents.txt")
    world.living_ents = control.db.entity.load_entities("living_ents.txt")

    # TODO: I should figure out a better way to set the dead room
    world.dead_room = world.tiles[(5, 3)]

    # put the entities on the map
    map_entities(world, world.basic_ents)
    map_entities(world, world.weapon_ents)
    map_entities(world, world.living_ents)
    map_entities(world, world.armour_ents)

    passwds = {}
    passwds["bob"] = "bob123"
    passwds["tim"] = "tim123"
    world.passwds = passwds

    # initialize spells
    simple_spells = control.db.spell.load_spells("spells.txt")
    world.spells = control.spells.initialize_spells(simple_spells)

    #FOR TESTING
    """
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
    """

    # enter main loop of the game
    control.socks.server_loop(world)

    control.db.entity.save_entities(world.basic_ents, "basic_ents.txt")
    control.db.entity.save_entities(world.weapon_ents, "weapon_ents.txt")
    control.db.entity.save_entities(world.armour_ents, "armour_ents.txt")
    control.db.entity.save_entities(world.living_ents, "living_ents.txt")

    """
    # commands I've tested:
    #res_spell = world.spells["resurrection"]
    #res_spell.cast(res_spell, world, bob, tim)
    #control.uinput.handle_user_input(world, bob, "cast heal at tim")
    #control.entities.cast_spell(world, world.entities[0], world.entities[1], "resurrection")
    #control.admin.make_tile(world, world.entities[0], (3, 0), "2x1")
    #control.mymap.display_map(world, world.entities[0])
    """
