#!/usr/bin/python3.4

import math
import queue
import control.roll
import model.util

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


# Most basic class:
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

    def send_msg(self, msg):
        print(msg)

    """
    This function can be used to heal or dmg a target.
    hp_change can be positive to heal someone or negative to hurt someone
    If the dst_entity dies, we will give exp to the src_entity and kill
    the dst_entity.
    """
    def change_hp(self, src_entity, hp_change):
        self.cur_hp = self.cur_hp + hp_change
        if self.cur_hp <= 0:
            src_entity.send_msg("You broke {}!".format(self.name))
            self.die()

    def die(self):
        pass


# Basic weapon:
class Weapon(Entity):

    def __init__(self):
        Entity.__init__(self)
        self.type = "weapon"      # the different entity classes
        # weapon dmg (2d6)
        self.die_to_roll = 0
        self.dmg_modifier = 0
        self.attack_bonus = 0
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


# Basic armour:
class Armour(Entity):

    def __init__(self):
        Entity.__init__(self)
        self.type = "armour"      # the different entity classes
        self.base_cost = 0
        self.armour_bonus = 0       # 1,2...
        self.max_dex_bonus = 8      # goes down from there
        self.armour_check_penalty = 0
        self.arcane_spell_fail = 5  # 5%, 10%...
        self.speed = (30, 20)       # different races have different speeds
        self.shield = False         # armour or shield
        self.armour_type = ""       # light, medium, heavy

# Basic living:
class Living(Entity):

    def __init__(self):
        Entity.__init__(self)
        self.type = "living"      # the different entity classes
        self.pclass = "fighter"
        self.cur_mp = 0
        self.max_mp = 10
        self.status_msgs = []
        self.vision_range = 5
        self.level = 0
        self.hit_dice = "2d4"
        self.race = "creature"
        # new
        self.attrib = {
            "str": (10, 0),
            "dex": (10, 0),
            "con": (10, 0),
            "int": (10, 0),
            "wis": (10, 0),
            "cha": (10, 0) }
        self.fortitude = {
            "total": 0,
            "base": 0,
            "magic": 0,
            "tmp": 0 }
        self.reflex = {
            "total": 0,
            "base": 0,
            "magic": 0,
            "tmp": 0 }
        self.will = {
            "total": 0,
            "base": 0,
            "magic": 0,
            "tmp": 0 }
        self.alignment = "neutral good"
        self.diety = "none"
        self.size = "medium"
        self.age = 21
        self.gender = "male"
        self.height = "6'2\""
        self.subdual_msg = 0
        self.arcane_spell_failure = 0
        self.armour_check_penalty = -4
        self.speed = 20
        self.attack_bonus = {
            "total": 3,
            "base": None,
            "misc": (0, None),  # first num will be the total, then []
                                #   of things that give the att bonus
            }
        self.ac = {
        #AC = 10 + armour bonus + shield bonus + dex mod + size mod + other
            "total": 0,
            "base": 10,
            "armour": 0,
            "shield": 0,
            "misc": (0, None),  # first num will be the total, then []
                                #   of things that give the att bonus
            }
        self.eq = {
            "left_hand": None,
            "right_hand": None,
            "armour": None,
            "helm": None,
            }
        self.skills = []
        self.spells = []
        self.feats = []
        self.ammunition = []
        self.inventory = []
        self.lift = {
            "over_head": 200,
            "off_ground": 600,
            "push_drag": 1000 }
        self.exp = 0
        self.money = 10

    def set_attrib(self, name, value):
        mod = math.floor((value-10)/2)
        self.attrib[name] = (value, mod)

    def can_move(self):
        can_move = True
        reason = None
        bad_statusi = ["lost balance", "paralyzed"]
        for bstate in bad_statusi:
            if bstate in self.status_msgs:
                can_move = False
                reason = bstate
        return (can_move, reason)

    #TODO: I think I'm gonna get rid of mp and have some kind of time thing
    def change_mp(self, mp_delta):
        self.cur_mp += mp_delta
        if self.cur_mp > self.max_mp:
            self.cur_mp = self.max_mp

    def add_status(self, status_msg):
        self.status_msgs.append(status_msg)

    def remove_status(self, status_msg):
        self.status_msgs.remove(status_msg)

    def get_attack_bonus(self, base_attack_bonus, melee=True, range_pen=0):
        # att_bonus = base_att_bonus + ability_mod + size_mod + misc
        # we'll do the d20 roll somehwere else

        if melee:
            attribute = "str"
        else:
            attribute = "dex"
        attrib, ability_mod = self.attrib[attribute]

        size_mod = model.util.size_modifiers[self.size]
        misc_attack_bonus, misc_list = self.attack_bonus["misc"]

        # attack_bonus (melee) = base_attack_bonus + str_mod + size_mod
        attack_bonus = base_attack_bonus + ability_mod + size_mod \
            + misc_attack_bonus
        # attack_bonus (ranged) = base_attack_bonus + dex_mod + size_mod
        #   + range_penalty
        if not melee:
            attack_bonus += range_pen

        return attack_bonus

    def wield(self, hand, item):
        hand = "{}_hand".format(hand)
        if self.eq.get(hand) is None:
            # there's nothing in that hand, so we can go ahead and wield it
            self.eq[hand] = item
            # need to check if the item even has an attack bonus
            if hasattr(item, "attack_bonus"):
                self.add_attack_bonus(item)
            # check to see if it has an AC bonus
            if hasattr(item, "armour_bonus") and \
                (item.armour_bonus is not None):
                # currently, I'm assuming shield are the only thing you
                #   can wield that will give AC bonus
                self.add_armour_bonus("shield", item.armour_bonus)
            #TODO: handle AC bonuses and other stuff
        #TODO: gotta figure out two-handed weapons

    def add_attack_bonus(self, item):
        total, misc_list = self.attack_bonus["misc"]
        total += item.attack_bonus
        if misc_list is None:
            misc_list = []
        misc_list.append(item)
        self.attack_bonus["misc"] = (total, misc_list)

    def remove_attack_bonus(self, item):
        misc_attack_bonus, misc_list = self.attack_bonus["misc"]
        misc_attack_bonus -= item.attack_bonus
        misc_list.remove(item)
        self.attack_bonus["misc"] = (misc_attack_bonus, misc_list)

    def calculate_ac(self):
        ac = self.ac
        dex, dex_mod = self.attrib["dex"]
        size_mod = model.util.size_modifiers[self.size]
        misc_mod, items = ac["misc"]

        # ac = 10 + armour_bonus + shield_bonus + dex_mod + size_mod + misc
        self.ac["total"] = ac["base"] + ac["armour"] + ac["shield"] + \
            dex_mod + size_mod + misc_mod

    def add_armour_bonus(self, bonus_type, amt, item=None):
        # types of bonus: total, base, armour, shield, misc
        status = 0
        if bonus_type in (set(self.ac.keys()) - set(["total", "base"])):
            if bonus_type == "misc":
                # misc (i.e. spells, rings/amulets...)
                if item is None:
                    status = 2
                else:
                    misc_amt, misc_list = self.ac["misc"]
                    misc_amt += amt
                    if misc_list is None:
                        misc_list = []
                    misc_list.append(item)
                    self.ac["misc"] = (misc_amt, misc_list)
            else:
                # handle everything else
                self.ac[bonus_type] = amt
        else:
            status = 1 # wrong/unknown bonus_type

        if status == 0:
            self.calculate_ac()

        return status

    def remove_armour_bonus(self, bonus_type, amt, item=None):
        # types of bonus: total, base, armour, shield, misc
        status = 0
        if bonus_type in (set(self.ac.keys()) - set(["total", "base"])):
            if bonus_type == "misc":
                # misc (i.e. spells, rings/amulets...)
                if item is None:
                    status = 2
                else:
                    misc_amt, misc_list = self.ac["misc"]
                    misc_amt -= amt
                    if item in misc_list:
                        misc_list.remove(item)
                    self.ac["misc"] = (misc_amt, misc_list)
            else:
                # handle everything else
                self.ac[bonus_type] = 0
        else:
            status = 1 # wrong/unknown bonus_type

        if status == 0:
            self.calculate_ac()

        return status

    def unwield(self, hand):
        hand = "{}_hand".format(hand)
        if self.eq.get(hand) is not None:
            item = self.eq[hand]
            self.eq[hand] = None
            if hasattr(item, "attack_bonus"):
                self.remove_attack_bonus(item)
            if hasattr(item, "armour_bonus"):
                # currently, I'm assuming shield are the only thing you
                #   can wield that will give AC bonus
                self.remove_armour_bonus("shield", item.armour_bonus, item)
                
    """
    This function can be used to heal or dmg a target.
    hp_change can be positive to heal someone or negative to hurt someone
    If the dst_entity dies, we will give exp to the src_entity and kill
    the dst_entity.
    """
    def change_hp(self, src_entity, hp_change):
        self.cur_hp = self.cur_hp + hp_change
        if self.cur_hp <= 0:
            src_entity.send_msg("You killed {}!".format(self.name))
            self.send_msg("Oh no! You died!")
            self.die()

    def die(self):
        self.add_status("dead")



class Humanoid(Living):

    def __init__(self):
        Living.__init__(self)
        # self.class = "ranger"
        # self.proficiency_bonus = 2 ?
        # self.armour = plate
        # self.helm = helmet
        # self.left_hand = shield
        # self.right_hand = sword

"""
    def die(self):
    def move(self):
"""


# Advanced Player:
class Player(Humanoid):

    def __init__(self):
        Humanoid.__init__(self)
        self.type = "player"        # the different entity classes
        self.sock = None
        self.msg_queue = queue.Queue()
        self.special_state = "login"    # this is to help with login process

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
I'll need to make sure I keep this up-to-date, which will suck, but
I don't know a better way to transfer info between objects.
"""
from copy import copy
def transfer_living_to_player(life, plife):

    # when a player disconnects from the game and then reconnects,
    #   their entity is a Player object. If that's the case, delete
    #   the player specific entires in the object and then transfer that
    """
    # this shouldn't happen any more...
    if life.type == "player":
        del(life.sock)
        del(life.msg_queue)
        del(life.special_state)
    """

    # copy over all the appropriate information from life to plife
    list_to_transfer = [entry for entry in dir(life)
        # make sure the variable name doesn't start with "__"
        if ((not entry.startswith("_")) and
            # make sure the variable isn't a function
            (not callable(life.__getattribute__(entry))))]
    #print("Before transfer:")
    for entry in list_to_transfer:
    #    print("{} : {}".format(entry, plife.__getattribute__(entry)))
        plife.__setattr__(entry, life.__getattribute__(entry))
    plife.type = "player"
    #print("After transfer:")
    #for entry in list_to_transfer:
    #    print("{} : {}".format(entry, plife.__getattribute__(entry)))

    # tell world to point to the player object now
    plife.world.living_ents[life.name] = plife
    # check to see if the life object is already on a tile then remove it
    tile = plife.world.tiles[plife.cur_loc]
    if life in tile.entities:
        tile.entities.remove(life)
    # add the plife to the tile
    tile.entities.append(plife)


"""
I'll need to make sure I keep this up-to-date, which will suck, but
I don't know a better way to transfer info between objects.
"""
def transfer_player_to_living(plife, life):

    del(plife.sock)
    del(plife.msg_queue)
    del(plife.special_state)
    plife.type = "living"

    # generate a list of variables to copy over
    list_to_transfer = [entry for entry in dir(life)
        # make sure the variable name doesn't start with "__"
        if ((not entry.startswith("_")) and
            # make sure the variable isn't a function
            (not callable(life.__getattribute__(entry))))]
    # copy the information from plife to life
    for entry in list_to_transfer:
        life.__setattr__(entry, plife.__getattribute__(entry))

    # tell world to point to the player object now
    life.world.living_ents[life.name] = life
    # check to see if the plife object is already on a tile then remove it
    tile = life.world.tiles[life.cur_loc]
    if plife in tile.entities:
        tile.entities.remove(plife)
    # add the life to the tile
    tile.entities.append(life)
    #TODO: there might be more places where I'll have to make the transfer
