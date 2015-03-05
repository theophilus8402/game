#!/usr/bin/python3.4

import queue

class Entity:

    def __init__(self):
        self.symbol = ""
        self.name = ""
        self.cur_loc = (0, 0)
        self.sock = None
        self.msg_queue = queue.Queue()
        self.messages = []
        self.hp = 0
        self.default_hp = 0
        """
        short_desc = ""
        long_desc = ""
        barrier = False
        mobile = True
        weight = 0
        """


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
        symbol = self.default_symbol
        if len(self.entities) > 0:
            symbol = self.entities[0].symbol
        return symbol
