#!/usr/bin/python3.4

import model.entity
import queue
import sys

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

