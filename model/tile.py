#!/usr/bin/python3.4

import math
import queue
import sys

import model.entity
from model.info import Status, Coord


def add_entity(tile, entity):
    """
    Checks if the entity can be added to the tile.
    Adds the entity to the tile, and updates the entity's coord.
    Returns the whether act of adding the entity was successful.
    """
    # here, I can check to see if there's enough space for the entity
    #   or other... stuff...
    status = Status.all_good
    # if there's no room in the tile, status = Status.no_room_in_tile
    tile.entities.append(entity)
    entity.coord = tile.coord
    return status


def remove_entity(tile, entity):
    """
    Removes the entity from the tile.  Returns Status.entity_not_in_tile if
    the entity is not there.
    """
    status = Status.all_good
    # make sure the entity was there in the first place
    if entity in tile.entities:
        tile.entities.remove(entity)
    else:
        status = Status.entity_not_in_tile
    return status


def check_tile_new_entity(tile, searching_entity):
    """
    Checks the given tile for a list of entities and makes sure it's not the calling
    entities name.  Adds each entity to the other's list of nearby entities.
    TODO: I don't think this quite enables us to have different entities with
    different visual ranges.
    MAYBE: I can have a large default visual range and then just check each time
    a message is sent if the entity can see the message.
    """
    for ent in tile.entities:
        if ent.name != searching_entity.name:
            searching_entity.peeps_nearby.add(ent)
            ent.peeps_nearby.add(searching_entity)
            #print("Saw {} at {}.".format(ent.name, coord))


class Tile:

    def __init__(self):
        self.uid = 0
        self.entities = []
        self.ground = ""    # muddy, water, rough
        self.coord = (0, 0)
        self.default_symbol = "."

    """
    If there is an entity in the tile, it's symbol will be returned.
    If there are no entities, the default_symbol will be returned.
    """
    def get_symbol(self):
        symbol = None
        living_symbol = None
        if len(self.entities) > 0:
            symbol = self.entities[0].symbol
            # look through all the entities
            for ent in self.entities:
                # if there's a player, use that symbol first
                if ent.type == "player":
                    symbol = ent.symbol
                    break
                # if there's a living creature, use that
                if (ent.type == "living") and not living_symbol:
                    living_symbol = ent.symbol
        if not symbol:
            if living_symbol:
                symbol = living_symbol
            else:
                symbol = self.default_symbol
        return symbol

