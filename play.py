#!/usr/bin/python3.4

import model.entity
import model.tile
import model.util

def make_shoe():
    shoe = model.entity.Entity()
    shoe.type = "entity"
    shoe.uid = 20
    shoe.name = "shoe"
    shoe.symbol = "*"
    shoe.cur_loc = (1, 3)
    shoe.cur_hp = 10
    shoe.max_hp = 10
    shoe.short_desc = "This is an old shoe."
    shoe.long_desc = "This is a really old shoe. It's floppy."
    shoe.weight = 1
    shoe.volume = .5
    shoe.friction = .1
    return shoe


def make_sword():
    sword = model.entity.Weapon()
    sword.uid = 21
    sword.name = "sword"
    sword.symbol = "-"
    sword.cur_loc = (1, 3)
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
    shield = model.entity.Armour()
    shield.uid = 24
    shield.name = "shield"
    shield.symbol = "o"
    shield.cur_loc = (-2, -1)
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


def make_plate():
    plate = model.entity.Armour()
    plate.uid = 23
    plate.name = "plate"
    plate.symbol = "&"
    plate.cur_loc = (-1, -1)
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
    dog = model.entity.Living()
    dog.uid = 44
    dog.name = "dog"
    dog.symbol = "d"
    dog.cur_loc = (-1, 2)
    dog.cur_hp = 7
    dog.max_hp = 7
    dog.short_desc = "This dog is annoying."
    dog.long_desc = "This is a mangy mut."
    dog.weight = 41
    dog.volume = 4
    dog.friction = 5
    dog.cur_mp = 0
    dog.max_mp = 0
    #dog.status_msgs = []
    dog.status_msgs = ["dumb", "hungry", "lost balance"]
    return dog


def make_bob():
    bob = model.entity.Humanoid()
    bob.uid = 1
    bob.name = "bob"
    bob.symbol = "B"
    bob.cur_loc = (1, 2)
    bob.cur_hp = 10
    bob.max_hp = 10
    bob.short_desc = "This is Bob."
    bob.long_desc = "This is Bob. He's rugged looking."
    bob.weight = 192
    bob.volume = 12
    bob.friction = 10
    bob.cur_mp = 10
    bob.max_mp = 10
    bob.vision_range = 6
    #bob.status_msgs = []
    bob.status_msgs = ["lost balance"]

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
        att_roll = control.roll.attack_roll(att_bonus)
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

