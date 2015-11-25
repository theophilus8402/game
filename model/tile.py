#!/usr/bin/python3.4

import math
import queue
import sys

import model.entity


def add_entity(tile, entity):
    # here, I can check to see if there's enough space for the entity
    #   or other... stuff...
    status = 0
    tile.entities.append(entity)
    return status


def remove_entity(tile, entity):
    status = 0
    # make sure the entity was there in the first place
    if entity in tile.entities:
        tile.entities.remove(entity)
    else:
        status = 6      # entity wasn't in tile.entities
    return status


NORTH = "n"
EAST = "e"
SOUTH = "s"
WEST = "w"
NORTHEAST = "ne"
SOUTHEAST = "se"
SOUTHWEST = "sw"
NORTHWEST = "nw"
PHYSICAL = "physical"
VISION = "vision"
HEARING = "hearing"
DEF_DST = 5
DIAG_DST = math.sqrt(DEF_DST**2 + DEF_DST**2)


def get_dist_nearby_tiles(tile1, direction, entity=None, distance_type=PHYSICAL,
    move_type="walk", object_to_climb=None):

    distance = 0

    if move_type == "walk":  #figure out movement for walking
        distance = tile1.distances[direction][distance_type]
    elif move_type == "climb":
        #figure something out for that
        pass

    return distance


class Tile:

    def __init__(self):
        self.uid = 0
        self.entities = []
        self.ground = ""    # muddy, water, rough
        self.coord = (0, 0)
        self.default_symbol = "."
        self.distances = {
            NORTH : {PHYSICAL : DEF_DST, VISION : DEF_DST, HEARING : DEF_DST},
            EAST : {PHYSICAL : DEF_DST, VISION : DEF_DST, HEARING : DEF_DST},
            SOUTH : {PHYSICAL : DEF_DST, VISION : DEF_DST, HEARING : DEF_DST},
            WEST : {PHYSICAL : DEF_DST, VISION : DEF_DST, HEARING : DEF_DST},
            NORTHEAST : {PHYSICAL : DIAG_DST, VISION : DIAG_DST, HEARING : DIAG_DST},
            SOUTHEAST : {PHYSICAL : DIAG_DST, VISION : DIAG_DST, HEARING : DIAG_DST},
            SOUTHWEST : {PHYSICAL : DIAG_DST, VISION : DIAG_DST, HEARING : DIAG_DST},
            NORTHWEST : {PHYSICAL : DIAG_DST, VISION : DIAG_DST, HEARING : DIAG_DST},
        }

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

