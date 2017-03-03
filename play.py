#!/usr/bin/python3.4

from model.entity.basic_entity import Entity
from model.entity.weapons import Weapon
from model.entity.armour import Armour
from model.entity.classes.fighter import Fighter
from model.entity.classes.mage import Mage
from model.entity.inventory import Inventory
from model.entity.living.actions import hit
from model.entity.living.humanoid import Humanoid
from model.entity.living.living import *
from model.entity.living.equip import *
from model.entity.living.blob import *
from model.entity.living.status_effects import *
from model.entity.races.human import Human
from model.entity.util import *
from model.info import Coord
from model.special_effect import Effect, SpecialEffect
from model.tile import *
from model.util import roll, RollType

prof = Proficiency

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


def make_shoes():
    shoes = Entity()
    shoes.type = "entity"
    shoes.eq_slot = EqSlots.right_leg
    shoes.uid = 20
    shoes.name = "shoes"
    shoes.symbol = "*"
    shoes.coord = Coord(2, 3)
    shoes.cur_hp = 10
    shoes.max_hp = 10
    shoes.short_desc = "This is a pair of old shoes."
    shoes.long_desc = "This is a  pair of really old shoes. They're floppy."
    shoes.weight = 1
    shoes.volume = .5
    shoes.friction = .1
    return shoes


def make_bow():
    bow = Weapon()
    bow.uid = 28
    bow.name = "short bow"
    bow.symbol = "D"
    bow.eq_slot = EqSlots.hand
    bow.coord = Coord(-1, 3)
    bow.cur_hp = 13
    bow.max_hp = 13
    bow.short_desc = "This is a spiffy short bow."
    bow.long_desc = "This is a really spiffy short bow."
    bow.weight = 6
    bow.volume = 1
    bow.friction = .3
    bow.die_to_roll = 2
    bow.dmg_modifier = 3
    bow.critical_range = 19
    bow.critical_dmg = 3
    bow.range_increment = 0
    bow.attack_bonus = 0
    bow.base_cost = 10
    bow.proficiency = Proficiency.simple_weapons
    bow.properties = [Property.ammunition, Property.two_handed]
    bow.melee = False
    bow.weapon_type = "short_bow"
    bow.dmg_type = "cutting"
    bow.size = "medium"
    bow.reach = False
    return bow


def make_sword():
    sword = Weapon()
    sword.uid = 21
    sword.name = "short sword"
    sword.eq_slot = EqSlots.hand
    sword.symbol = "-"
    sword.coord = Coord(1, 3)
    sword.cur_hp = 13
    sword.max_hp = 13
    sword.short_desc = "This is a shiny short sword."
    sword.long_desc = "This is a really shiny short sword. It is not floppy."

    sword.possibilities[RollType.hit] = 5
    sword.possibilities[RollType.critical_hit] = 5

    sword.weight = 6
    sword.volume = 1
    sword.friction = .3
    sword.die_to_roll = 2
    sword.dmg_per_die = 4
    sword.dmg_modifier = 1
    sword.critical_dmg = 3
    sword.range_increment = 0
    sword.base_cost = 10
    sword.proficiency = Proficiency.martial_weapons
    sword.properties = [Property.finesse, Property.light]
    sword.melee = True
    sword.weapon_type = "short_sword"
    sword.dmg_type = "cutting"
    sword.size = "medium"
    sword.reach = False
    sword.two_handed = False
    return sword


def make_shield():
    shield = Armour()
    shield.uid = 24
    shield.name = "shield"
    shield.symbol = "o"
    shield.eq_slot = EqSlots.hand
    shield.coord = Coord(-2, -1)
    shield.cur_hp = 20
    shield.max_hp = 20
    shield.short_desc = "This is a small, wooden shield."
    shield.long_desc = "This is a nice, small, wooden shield."

    shield.possibilities[RollType.block] = 5
    block_effect = SpecialEffect(Effect.block)
    block_effect.block_value = 2
    shield.special_effects.add(block_effect)

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
    shield.proficiency = Proficiency.shields
    shield.properties = []
    return shield


def make_armour():
    plate = Armour()
    plate.uid = 23
    plate.name = "plate"
    plate.symbol = "&"
    plate.eq_slot = EqSlots.torso
    plate.coord = Coord(-1, -1)
    plate.cur_hp = 20
    plate.max_hp = 20
    plate.short_desc = "This is a spiffy suite of plate mail armour."
    plate.long_desc = "This is a really spiffy suite of plate mail armour."

    plate.possibilities[RollType.block] = 5

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
    plate.proficiency = Proficiency.heavy_armour
    plate.properties = []
    return plate


def make_dog():
    dog = Living()
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
    dog.male = True
    return dog


def make_bob():
    bob = Humanoid()
    bob.uid = 1
    bob.name = "Bob"
    bob.symbol = "B"
    bob.coord = Coord(1, 2)
    bob.cur_hp = 10
    bob.max_hp = 10
    bob.short_desc = "This is Bob."
    bob.long_desc = "This is Bob. He's rugged looking."
    bob.male = True
    bob.weight = 192
    bob.volume = 12
    bob.friction = 10
    bob.cur_mp = 10
    bob.max_mp = 10
    bob.male = True

    #bob.blob_state = BlobState(States.expect_login_name)

    bob.known_cmds = CMDS_BASIC_MOVEMENT.union(CMDS_BASIC_ATTACK)
    bob.known_cmds = bob.known_cmds.union(CMDS_BASIC_HUMANOID)
    bob.known_cmds = bob.known_cmds.union(CMDS_DEBUG)

    #add_status_effect(bob, Blessings.game_master)

    bob.pclass = Class.fighter
    bob.level = 10
    bob.abilities = {}
    set_ability(bob, Ability.strength, 14)
    set_ability(bob, Ability.dexterity, 15)
    set_ability(bob, Ability.constitution, 13)
    set_ability(bob, Ability.intelligence, 11)
    set_ability(bob, Ability.wisdom, 11)
    set_ability(bob, Ability.charisma, 10)
    bob.proficiencies = [prof.light_armour, prof.medium_armour, prof.heavy_armour,
        prof.shields, prof.simple_weapons, prof.martial_weapons]
    bob.size = "small"
    return bob


def make_tim():
    tim = Humanoid()
    tim.uid = 2
    tim.name = "Tim"
    tim.symbol = "T"
    tim.coord = Coord(2, 2)
    tim.cur_hp = 10
    tim.max_hp = 10
    tim.short_desc = "This is Tim."
    tim.long_desc = "This is Tim. He's not rugged looking."
    tim.male = True
    tim.weight = 192
    tim.volume = 12
    tim.friction = 10
    tim.cur_mp = 10
    tim.max_mp = 10
    #add_status_effect(tim, Afflictions.lost_balance)
    tim.male = True

    tim.known_cmds = CMDS_BASIC_MOVEMENT.union(CMDS_BASIC_ATTACK)

    tim.pclass = Class.wizard
    tim.level = 10
    tim.abilities = {}
    set_ability(tim, Ability.strength, 11)
    set_ability(tim, Ability.dexterity, 12)
    set_ability(tim, Ability.constitution, 10)
    set_ability(tim, Ability.intelligence, 18)
    set_ability(tim, Ability.wisdom, 16)
    set_ability(tim, Ability.charisma, 13)
    tim.proficiencies = [prof.light_armour, prof.medium_armour, prof.heavy_armour,
        prof.shields, prof.simple_weapons, prof.martial_weapons]
    tim.size = "small"
    return tim


def make_alice():
    alice = Humanoid()
    alice.uid = 2
    alice.name = "Alice"
    alice.symbol = "A"
    alice.coord = Coord(3, -2)
    alice.cur_hp = 10
    alice.max_hp = 10
    alice.short_desc = "This is Alice."
    alice.long_desc = "This is Alice.  She is a woman."
    alice.male = False
    alice.weight = 142
    alice.volume = 12
    alice.friction = 10
    alice.cur_mp = 10
    alice.max_mp = 10
    alice.male = False

    alice.known_cmds = CMDS_BASIC_MOVEMENT.union(CMDS_BASIC_ATTACK)

    alice.level = 10
    alice.pclass = Class.rogue
    alice.abilities = {}
    set_ability(alice, Ability.strength, 8)
    set_ability(alice, Ability.dexterity, 18)
    set_ability(alice, Ability.constitution, 11)
    set_ability(alice, Ability.intelligence, 17)
    set_ability(alice, Ability.wisdom, 14)
    set_ability(alice, Ability.charisma, 16)
    alice.proficiencies = [prof.light_armour, prof.medium_armour, prof.heavy_armour,
        prof.shields, prof.simple_weapons, prof.martial_weapons]
    alice.size = "small"
    return alice


def make_new_bob():
    new_bob = NewLiving()
    new_bob.race = Human()
    new_bob.class_type = Fighter()
    new_bob.equipment = HumanoidEquipment()
    new_bob.inventory = Inventory()
    return new_bob


def make_new_tim():
    new_tim = NewLiving()
    new_tim.race = Human()
    new_tim.class_type = Mage()
    new_tim.equipment = HumanoidEquipment()
    new_tim.inventory = Inventory()
    return new_tim


if __name__ == "__main__":

    shoe = make_shoes()
    sword = make_sword()
    shield = make_shield()
    plate = make_armour()
    dog = make_dog()
    bob = make_new_bob()
    tim = make_new_tim()
    #bob.wield("right", sword)
    #print("Wield sword in right hand...")
    #bob.wield("left", shield)
    #print("Wield shield in left hand...")
    #print()

    bobs_info = get_roll_possibilities(bob)

    bob.inventory.add_item(sword)
    bob.equip(sword, EqSlots.right_hand)

    tim.inventory.add_item(plate)
    tim.inventory.add_item(shield)
    tim.equip(plate, EqSlots.torso)
    tim.equip(shield, EqSlots.left_hand)

    """
    print()
    bob.unwield("right")
    print("Unwielding right hand...")
    bob.unwield("left")
    print("Unwielding shield in left hand...")
    print()

    info.show_ac(bob)
    print()

    for att_bonus in bob.get_attack_bonus(melee=True):
        att_roll = model.util.roll(1, 20, att_bonus)
        print("att_roll = {} + {} = {}".format(att_roll-att_bonus,
            att_bonus, att_roll))
    """

