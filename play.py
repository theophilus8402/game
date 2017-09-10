#!/usr/bin/python3.4

from model.entity.armor import Armor
from model.entity.basic_entity import Entity
from model.entity.classes.util import ClassName
from model.entity.damage import DmgType
from model.entity.inventory import Inventory
from model.entity.living.actions import hit
from model.entity.living.ability_scores import *
from model.entity.living.armor_class import ArmorBonus,ArmorClass
from model.entity.living.attack_bonus import AttackBonus,BaseAttackBonus
from model.entity.living.races import *
from model.entity.living.humanoid import Humanoid
from model.entity.living.living import *
from model.entity.living.equip import *
from model.entity.living.blob import *
from model.entity.living.status_effects import *
from model.entity.util import *
from model.entity.weapons import Weapon
from model.info import Coord
from model.special_effect import Effect, SpecialEffect
from model.tile import *
from model.world import World
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
    world = World()
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
    sword.damage = {DmgType.slashing: (6, 2)}

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
    shield = Armor()
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
    plate = Armor()
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

#
#def make_dog():
#    dog = Living()
#    dog.uid = 44
#    dog.name = "dog"
#    dog.symbol = "d"
#    dog.coord = Coord(-1, 2)
#    dog.cur_hp = 7
#    dog.max_hp = 7
#    dog.short_desc = "This dog is annoying."
#    dog.long_desc = "This is a mangy mut."
#    dog.weight = 41
#    dog.volume = 4
#    dog.friction = 5
#    dog.cur_mp = 0
#    dog.max_mp = 0
#    add_status_effect(dog, Afflictions.stupid)
#    add_status_effect(dog, Afflictions.lost_balance)
#    dog.known_cmds = CMDS_BASIC_MOVEMENT.union(CMDS_BASIC_HUMANOID)
#    dog.male = True
#    return dog
#

def make_bob():
    str_bonus = AbilityBonus(Ability.str, 2, BonusReason.race)
    ability_scores = [
        AbilityScore(Ability.str, 17),
        AbilityScore(Ability.dex, 14),
        AbilityScore(Ability.con, 13),
        AbilityScore(Ability.wis, 12),
        AbilityScore(Ability.int, 8),
        AbilityScore(Ability.cha, 12),
        ]
    human = Human(str_bonus)
    fighter = ClassName.fighter
    bob = Living(ab_scores=ability_scores, race=human, class_name=fighter)
    bob.name = "bob"

    return bob


def make_tim():
    ability_scores = [
        AbilityScore(Ability.str, 10),
        AbilityScore(Ability.dex, 14),
        AbilityScore(Ability.con, 12),
        AbilityScore(Ability.wis, 13),
        AbilityScore(Ability.int, 8),
        AbilityScore(Ability.cha, 16),
        ]
    wizard = ClassName.wizard
    tim = Living(ab_scores=ability_scores, race=Halfling(), class_name=wizard)
    tim.name = "tim"

    armor_bonus = ArmorBonus(10, BonusReason.armor_bonus)
    tim.add_bonus(armor_bonus)

    return tim


if __name__ == "__main__":

    shoe = make_shoes()
    sword = make_sword()
    shield = make_shield()
    plate = make_armour()
    #dog = make_dog()
    bob = make_bob()
    tim = make_tim()
    #bob.wield("right", sword)
    #print("Wield sword in right hand...")
    #bob.wield("left", shield)
    #print("Wield shield in left hand...")
    #print()

    bob.inventory.add_item(sword)
    bob.equip(sword, EqSlots.right_hand)

    tim.inventory.add_item(plate)
    tim.inventory.add_item(shield)
    tim.equip(plate, EqSlots.torso)
    tim.equip(shield, EqSlots.left_hand)

    world = make_world()
    world.living_ents[tim.name] = tim
    world.living_ents[bob.name] = bob


