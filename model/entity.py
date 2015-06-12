#!/usr/bin/python3.4

import queue
import sys

"""
Types of Entities:
    1) basic item (i.e. chairs, walls, trees, bushes, swords, arrows, food)
        * really, all items could have:
            dmg, durability/hp, weight, volume...
        * but, swords and equipment might have different properties
    2) live entities
        a) computer controlled (might have a socket in future to offload
            entities to other computers)
        b) the player (these two guys differ significantly in how you
            display/handle information and actions available
"""


"""
Most basic class:
"""
class Entity:

    def __init__(self):
        # stuff stored in db in order
        self.uid = 0 # TODO: implement this more
        self.name = None
        self.type = "entity"      # the different entity classes
        self.symbol = ""
        self.cur_loc = (0, 0)
        self.cur_hp = 0
        self.max_hp = 10

        self.short_desc = ""
        self.long_desc = ""
        self.weight = 0
        self.volume = 0          # this is how we will block movement
                            # a 5ftx5ftx10ft room is a max 250ft^3
        self.friction = 0

        # stuff not stored in db
        self.world = None

    #def change_hp():


"""
Basic weapon:
class Weapon(Entity):

    def __init__(self):
        self.type = "weapon"      # the different entity classes
        # weapon dmg (2d6)
        self.die_to_roll = 0
        self.dmg_modifier = 0
        self.critical_range = 20    # can be 19-20
        self.critical_dmg = 2       # x2
        self.range_increment = 0    # stuff for projectiles
        self.base_cost = 0          # can be modified
        self.weapon_category = ""   # simple, martial, exotic
        self.melee = True           # melee or ranged
        self.weapon_type = ""       # sword, mace
        self.dmg_type = []          # blunt, pierce (can be a combo of em)
        self.size = ""              # tiny, small, medium, large
        self.reach = False          # i.e. glaive can hit 10ft away but not
                                    #   right infront
        self.two_handed = False     # this is only for absolute reqs
                                    #   this doesn't handle large weapon
                                    #   being wielded by a gnome


Basic armour:
class Armour(Entity):

    def __init__(self):
        self.type = "armour"      # the different entity classes
        self.base_cost = 0
        self.armour_bonus = 0       # 1,2...
        self.max_dex_bonus = 8      # goes down from there
        self.armour_check_penalty = 0
        self.arcane_spell_fail = 5  # 5%, 10%...
        self.speed = 30/20          # different races have different speeds
        self.shield = False         # armour or shield
        self.armour_type = ""       # light, medium, heavy

Basic living:
class Living(Entity):

    def __init__(self):
        self.type = "living"      # the different entity classes
        self.cur_mp = 0
        self.max_mp = 10

    def move():

    def change_mp():


Advanced Player:
class Player(Living):

    def __init__(self):
        self.type = "player"      # the different entity classes
        self.sock = None
        self.msg_queue = queue.Queue()
        # the following two items are set so that user can login
        self.special_state = True
        self.state = "login"
        self.status_msgs = []

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
"""
