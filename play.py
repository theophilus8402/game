#!/usr/bin/python3.4

from model.entity.basic_entity import Entity
from model.entity.classes import ClassName
from model.entity.living.ability_scores import *
from model.entity.living.armor_class import ArmorBonus,ArmorClass
from model.entity.living.races import *
from model.entity.living.living import *
from model.entity.living.equip import *
from model.entity.living.status_effects import *
from model.entity.living.feats import *
from model.entity.util import *
from model.entity.weapons import *
from model.world import World
from model.map import Map,Coord
from model.util import roll

prof = Proficiency

def mtile(uid, coord):
    tile = Tile()
    tile.uid = uid
    tile.coord = coord
    return tile


def make_world():
    # create the temporary world (it is a 4x4 world)
    world = World()
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
    barbarian = ClassName.barbarian
    bob = Living(ab_scores=ability_scores, race=human, class_name=barbarian)
    bob.name = "bob"
    bob.symbol = "B"
    bob.permanent = True

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
    tim.symbol = "T"

    armor_bonus = ArmorBonus(10, BonusReason.armor_bonus)
    tim.add_bonus(armor_bonus)

    tim.permanent = True

    return tim


if __name__ == "__main__":

    #dog = make_dog()
    bob = make_bob()
    tim = make_tim()

    small_dagger = Dagger(Size.small)
    medium_dagger = Dagger(Size.medium)

    bob.inventory.add_item(medium_dagger)
    bob.equip(medium_dagger, EqSlots.right_hand)

    tim.inventory.add_item(small_dagger)
    tim.equip(small_dagger, EqSlots.right_hand)

    world = make_world()
    world.living_ents[tim.name] = tim
    world.living_ents[bob.name] = bob

    world.map = Map((-3, 6), (5, -4), ".")
    world.map.add_symbol(Coord(0, 0), "0")

    world.place_entity(bob, Coord(1, 2))
    world.place_entity(tim, Coord(2, 2))

