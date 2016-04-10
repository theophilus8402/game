#!/usr/bin/python3.4

import model.entity.entity
from model.entity.living import *
from model.entity.status_effects import *
from model.tile import *
from model.info import Coord
import model.util

def mtile(uid, coord):
    tile = Tile()
    tile.uid = uid
    tile.coord = coord
    return tile


def make_world():
    # create the temporary world (it is a 4x4 world)
    dim = 4
    uuid = 0
    world = model.world.World()
    for y in range(-dim, dim+1):
        for x in range(-dim, dim+1):
            world.tiles[Coord(x,y)] = mtile(uuid, Coord(x,y))
            uuid = uuid+1
    return world


def make_shoe():
    shoe = model.entity.entity.Entity()
    shoe.type = "entity"
    shoe.uid = 20
    shoe.name = "shoe"
    shoe.symbol = "*"
    shoe.coord = Coord(1, 3)
    shoe.cur_hp = 10
    shoe.max_hp = 10
    shoe.short_desc = "This is an old shoe."
    shoe.long_desc = "This is a really old shoe. It's floppy."
    shoe.weight = 1
    shoe.volume = .5
    shoe.friction = .1
    return shoe


def make_sword():
    sword = model.entity.entity.Weapon()
    sword.uid = 21
    sword.name = "sword"
    sword.symbol = "-"
    sword.coord = Coord(1, 3)
    sword.cur_hp = 13
    sword.max_hp = 13
    sword.short_desc = "This is a shiny sword."
    sword.long_desc = "This is a really shiny sword. It is not floppy."
    sword.weight = 6
    sword.volume = 1
    sword.friction = .3
    sword.die_to_roll = 2
    sword.dmg_modifier = 3
    sword.critical_range = 19
    sword.critical_dmg = 3
    sword.range_increment = 0
    sword.attack_bonus = 1
    sword.base_cost = 10
    sword.weapon_category = "martial"
    sword.melee = True
    sword.weapon_type = "sword"
    sword.dmg_type = "cutting"
    sword.size = "medium"
    sword.reach = False
    sword.two_handed = False
    return sword


def make_shield():
    shield = model.entity.entity.Armour()
    shield.uid = 24
    shield.name = "shield"
    shield.symbol = "o"
    shield.coord = Coord(-2, -1)
    shield.cur_hp = 20
    shield.max_hp = 20
    shield.short_desc = "This is a small, wooden shield."
    shield.long_desc = "This is a nice, small, wooden shield."
    shield.weight = 5
    shield.volume = 3
    shield.friction = 1
    shield.base_cost = 3
    shield.armour_bonus = 1
    shield.max_dex_bonus = None
    shield.armour_check_penalty = -1
    shield.arcane_spell_fail = 5
    shield.speed = None
    shield.shield = True
    shield.armour_type = "shield"
    return shield


def make_armour():
    plate = model.entity.entity.Armour()
    plate.uid = 23
    plate.name = "plate"
    plate.symbol = "&"
    plate.coord = Coord(-1, -1)
    plate.cur_hp = 20
    plate.max_hp = 20
    plate.short_desc = "This is a spiffy suite of plate mail armour."
    plate.long_desc = "This is a really spiffy suite of plate mail armour."
    plate.weight = 19
    plate.volume = 6
    plate.friction = 1
    plate.base_cost = 90
    plate.armour_bonus = 5
    plate.max_dex_bonus = 2
    plate.armour_check_penalty = 15
    plate.arcane_spell_fail = 25
    plate.speed = (30, 20)
    plate.shield = False
    plate.armour_type = "heavy"
    return plate


def make_dog():
    dog = model.entity.entity.Living()
    dog.uid = 44
    dog.name = "dog"
    dog.symbol = "d"
    dog.coord = Coord(-1, 2)
    dog.cur_hp = 7
    dog.max_hp = 7
    dog.short_desc = "This dog is annoying."
    dog.long_desc = "This is a mangy mut."
    dog.weight = 41
    dog.volume = 4
    dog.friction = 5
    dog.cur_mp = 0
    dog.max_mp = 0
    add_status_effect(dog, Afflictions.stupid)
    add_status_effect(dog, Afflictions.lost_balance)
    dog.known_cmds = CMDS_BASIC_MOVEMENT.union(CMDS_BASIC_HUMANOID)
    return dog


def make_bob():
    bob = model.entity.entity.Humanoid()
    bob.uid = 1
    bob.name = "bob"
    bob.symbol = "B"
    bob.coord = Coord(1, 2)
    bob.cur_hp = 10
    bob.max_hp = 10
    bob.short_desc = "This is Bob."
    bob.long_desc = "This is Bob. He's rugged looking."
    bob.weight = 192
    bob.volume = 12
    bob.friction = 10
    bob.cur_mp = 10
    bob.max_mp = 10

    bob.known_cmds = CMDS_BASIC_MOVEMENT.union(CMDS_BASIC_ATTACK)
    bob.known_cmds = bob.known_cmds.union(CMDS_BASIC_HUMANOID)
    bob.known_cmds = bob.known_cmds.union(CMDS_DEBUG)

    bob.pclass = "fighter"
    bob.level = 10
    bob.set_attrib("str", 14)
    bob.set_attrib("dex", 15)
    bob.set_attrib("con", 13)
    bob.set_attrib("int", 11)
    bob.set_attrib("wis", 11)
    bob.set_attrib("cha", 10)
    bob.attack_bonus["base"] = model.util.get_bab(bob.pclass, bob.level)
    bob.size = "small"
    return bob


def make_tim():
    tim = model.entity.entity.Humanoid()
    tim.uid = 2
    tim.name = "tim"
    tim.symbol = "T"
    tim.coord = Coord(2, 2)
    tim.cur_hp = 10
    tim.max_hp = 10
    tim.short_desc = "This is Tim."
    tim.long_desc = "This is Tim. He's not rugged looking."
    tim.weight = 192
    tim.volume = 12
    tim.friction = 10
    tim.cur_mp = 10
    tim.max_mp = 10
    add_status_effect(tim, Afflictions.lost_balance)

    tim.known_cmds = CMDS_BASIC_MOVEMENT.union(CMDS_BASIC_ATTACK)

    tim.pclass = "fighter"
    tim.level = 10
    tim.set_attrib("str", 11)
    tim.set_attrib("dex", 12)
    tim.set_attrib("con", 10)
    tim.set_attrib("int", 18)
    tim.set_attrib("wis", 16)
    tim.set_attrib("cha", 13)
    tim.attack_bonus["base"] = model.util.get_bab(tim.pclass, tim.level)
    tim.size = "small"
    return tim


if __name__ == "__main__":

    shoe = make_shoe()
    sword = make_sword()
    shield = make_shield()
    plate = make_plate()
    dog = make_dog()
    bob = make_bob()
    bob.wield("right", sword)
    print("Wield sword in right hand...")
    bob.wield("left", shield)
    print("Wield shield in left hand...")
    print()

    for att_bonus in bob.get_attack_bonus(melee=True):
        att_roll = model.roll.roll(1, 20, att_bonus)
        print("att_roll = {} + {} = {}".format(att_roll-att_bonus,
            att_bonus, att_roll))
    print()

    from view.entity import info
    bob.calculate_ac()
    info.show_ac(bob)

    print()
    bob.unwield("right")
    print("Unwielding right hand...")
    bob.unwield("left")
    print("Unwielding shield in left hand...")
    print()

    info.show_ac(bob)
    print()

    for att_bonus in bob.get_attack_bonus(melee=True):
        att_roll = control.roll.attack_roll(att_bonus)
        print("att_roll = {} + {} = {}".format(att_roll-att_bonus,
            att_bonus, att_roll))

