#!/usr/bin/python3.4

import queue
import sys

class Entity:

    def __init__(self):
        # stuff stored in db in order
        self.entity_uid = 0 # TODO: implement this more
        self.name = None
        self.symbol = ""
        self.cur_loc = (0, 0)
        self.hp = 0
        self.default_hp = 0 # TODO: change this to max_hp
        self.vision_range = 5

        # stuff not stored in db
        self.sock = None
        self.msg_queue = queue.Queue()
        # the following two items are set so that user can login
        self.special_state = True
        self.state = "login"
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


class World:

    def __init__(self):
        stdin = Entity()
        stdin.name = "stdin"
        stdin.sock = sys.stdin
        stdin.special_state = False
        stdin.state = None

        # key is the socket, value is the Entity
        self.sock_peeps = {}
        self.sock_peeps[sys.stdin] = stdin

        self.outputs = []
        self.passwds = {}        # key is name, passwd is value

        self.tiles = {}
        self.entities = []
