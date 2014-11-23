#!/usr/bin/python3.4

class Entity:
    symbol = ""
    name = ""
    cur_loc_x = 0
    cur_loc_y = 0
    """
    short_desc = ""
    long_desc = ""
    barrier = False
    mobile = True
    weight = 0
    """

    def __init__(self):
        self.symbol = ""
        self.name = ""
        self.cur_loc_x = 0
        self.cur_loc_y = 0


class Tile:
    uid = 0
    entities = []
    ground = ""         # muddy, water, rough
    default_symbol = "."
    x = 0
    y = 0

    def __init__(self):
        self.uid = 0
        self.entities = []
        self.ground = ""

    def get_symbol(self):
        symbol = self.default_symbol
        if len(self.entities) > 0:
            symbol = self.entities[0].symbol
        return symbol
