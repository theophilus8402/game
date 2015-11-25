import model.entity.entity
import model.tile
import sys

class World:

    def __init__(self):
        stdin = model.entity.entity.Entity()
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
        self.basic_ents = {}
        self.weapon_ents = {}
        self.armour_ents = {}
        self.living_ents = {}
        self.spells = {}

        # these max uids are the current highest uid
        # so, to create a new uid, return max_uid++
        self.max_tile_uid = 0
        self.max_ent_uid = 0

        self.msgs = []

    # tile commands
    tile_add_entity = model.tile.add_entity
    tile_remove_entity = model.tile.remove_entity

    def add_msg(self, msg):
        self.msgs.append(msg)

    def remove_msg(self, msg):
        self.msgs.remove(msg)

    def run_msgs(self):
        for msg in self.msgs:
            if msg.check():
                recurring = msg.execute()
                if not recurring:
                    self.remove_msg(msg)

    def get_new_tile_uid(self):
        self.max_tile_uid += 1
        return self.max_tile_uid

    def get_new_ent_uid(self):
        self.max_ent_uid += 1
        return self.max_ent_uid

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
