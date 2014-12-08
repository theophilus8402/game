#!/usr/bin/python3.4

class Entity:
    symbol = ""
    name = ""
    cur_loc_x = 0
    cur_loc_y = 0
    map_win = None
    text_win = None
    cmd_win = None
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
        self.map_win = None
        self.text_win = None
        self.cmd_win = None
        self.messages = []
        self.msg_len = 3000
        self.msg_start = 0


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
        self.x = 0
        self.y = 0

    def get_symbol(self):
        symbol = self.default_symbol
        if len(self.entities) > 0:
            symbol = self.entities[0].symbol
        return symbol
