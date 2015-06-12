#!/usr/bin/python3.4

import queue
import sys


class Entity:

    def __init__(self):
        # stuff stored in db in order
        self.uid = 0 # TODO: implement this more
        self.name = None
        self.symbol = ""
        self.cur_loc = (0, 0)
        self.cur_hp = 0
        self.max_hp = 10
        self.cur_mp = 0
        self.max_mp = 10
        self.vision_range = 5

        # stuff not stored in db
        self.world = None
        self.sock = None
        self.msg_queue = queue.Queue()
        # the following two items are set so that user can login
        self.special_state = "login"
        self.status_msgs = []
        """
        short_desc = ""
        long_desc = ""
        barrier = False
        mobile = True
        weight = 0
        """

    def change_mp(self, num):
        self.cur_mp += num
        if self.cur_mp > self.max_mp:
            self.cur_mp = self.max_mp

    # msg should always be a string with no '\n'
    def send_msg(self, msg):
        # I'm adding the ability to send msg to the local screen
        # this should help with testing.  I shouldn't need it in the future
        # so, I can get rid of this feature later and just have it send
        # stuff via a socket.
        if self.sock:
            bmsg = b''
            try:
                # make sure msg is a bytearray
                # will error if msg is already a bytearray
                bmsg = bytearray("{}\n".format(msg), "utf-8")
            except:
                bmsg = msg + b'\n'
            self.msg_queue.put(bmsg)
            if self.sock not in self.world.outputs:
                self.world.outputs.append(self.sock)
        else:
            print(msg)
        return True


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
        self.entities = {}
        self.spells = {}

        # these max uids are the current highest uid
        # so, to create a new uid, return max_uid++
        self.max_tile_uid = 0
        self.max_entity_uid = 0

    def get_new_tile_uid(self):
        self.max_tile_uid += 1
        return self.max_tile_uid

    def find_entity(self, name):
        name = name.lower()
        entity = self.living_ents.get(name)
        if not entity:
            entity = self.weapon_ents.get(name)
        if not entity:
            entity = self.armour_ents.get(name)
        if not entity:
            entity = self.basic_ents.get(name)
        return entity
