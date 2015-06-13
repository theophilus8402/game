#!/usr/bin/python3.4

import re
import model.entity

def save_entity(entity, file_handle):
    file_handle.write("type: {}\n".format(entity.type))
    file_handle.write("uid: {}\n".format(entity.uid))
    file_handle.write("name: {}\n".format(entity.name))
    file_handle.write("symbol: {}\n".format(entity.symbol))
    file_handle.write("cur_loc: {}\n".format(entity.cur_loc))
    file_handle.write("hp: {}/{}\n".format(entity.cur_hp, entity.max_hp))
    file_handle.write("short_desc: {}\n".format(entity.short_desc))
    file_handle.write("long_desc: {}\n".format(entity.long_desc))
    file_handle.write("weight: {}\n".format(entity.weight))
    file_handle.write("volume: {}\n".format(entity.volume))
    file_handle.write("friction: {}\n".format(entity.friction))
    return True


def save_weapon(entity, file_handle):
    # not writing the type because the save_entity func will do it for us
    file_handle.write("die_to_roll: {}\n".format(entity.die_to_roll))
    file_handle.write("dmg_modifier: {}\n".format(entity.dmg_modifier))
    file_handle.write("critical_range: {}\n".format(entity.critical_range))
    file_handle.write("critical_dmg: {}\n".format(entity.critical_dmg))
    file_handle.write("range_increment: {}\n".format(entity.range_increment))
    file_handle.write("base_cost: {}\n".format(entity.base_cost))
    file_handle.write("weapon_category: {}\n".format(entity.weapon_category))
    file_handle.write("melee: {}\n".format(entity.melee))
    file_handle.write("weapon_type: {}\n".format(entity.weapon_type))
    file_handle.write("dmg_type: {}\n".format(entity.dmg_type))
    file_handle.write("size: {}\n".format(entity.size))
    file_handle.write("reach: {}\n".format(entity.reach))
    file_handle.write("two_handed: {}\n".format(entity.two_handed))
    return True


def save_armour(entity, file_handle):
    # not writing the type because the save_entity func will do it for us
    file_handle.write("base_cost: {}\n".format(entity.base_cost))
    file_handle.write("armour_bonus: {}\n".format(entity.armour_bonus))
    file_handle.write("max_dex_bonus: {}\n".format(entity.max_dex_bonus))
    file_handle.write("armour_check_penalty: {}\n".format(entity.armour_check_penalty))
    file_handle.write("arcane_spell_fail: {}\n".format(entity.arcane_spell_fail))
    file_handle.write("speed: {}\n".format(entity.speed))
    file_handle.write("shield: {}\n".format(entity.shield))
    file_handle.write("armour_type: {}\n".format(entity.armour_type))


def save_living(entity, file_handle):
    # not writing the type because the save_entity func will do it for us
    file_handle.write("mp: {}/{}\n".format(entity.cur_mp, entity.max_mp))
    file_handle.write("status_msgs: {}\n".format(",".join(entity.status_msgs)))
    file_handle.write("vision_range: {}\n".format(entity.vision_range))
    file_handle.write("level: {}\n".format(entity.level))
    file_handle.write("hit_dice: {}\n".format(entity.hit_dice))
    file_handle.write("race: {}\n".format(entity.race))
    file_handle.write("str: {} dex: {} wis: {} con: {} int: {} cha: {}\n"\
        .format(entity.str, entity.dex, entity.wis, entity.con, entity.int,
        entity.cha))
 

def save_entities(entities, file_name):
    with open(file_name, "w") as f:
        for entity_name in entities:
            entity = entities[entity_name]
            # we are changing the type from player to living to better
            #   enable us to log in as anyone (a player or a dog...)
            if entity.type == "player":
                entity.type = "living"

            # now, save the data!!
            save_entity(entity, f)
            if entity.type == "armour":
                save_armour(entity, f)
            elif entity.type == "weapon":
                save_weapon(entity, f)
            elif entity.type == "living":
                save_living(entity, f)
            elif entity.type == "player":
                save_living(entity, f)
                # for now player doesn't have anything extra to save
                # but, of course this might change
            f.write("-------------------\n")


def load_entities(file_name):

    # basic entity
    re_uid = re.compile("uid: (\d+)")
    re_name = re.compile("name: (\w+)")
    re_type = re.compile("type: (\w+)")
    re_symbol = re.compile("symbol: (.+)")
    re_cur_loc = re.compile("cur_loc: \(([-0-9]+), ([-0-9]+)\)")
    re_hp = re.compile("hp: ([-0-9]+)/([-0-9]+)")
    re_short_desc = re.compile("short_desc: (.+)")
    re_long_desc = re.compile("long_desc: (.+)")
    re_weight = re.compile("weight: (\d+)")
    re_volume = re.compile("volume: (\d+)")
    re_friction = re.compile("friction: (\d+)")
    # weapon
    re_die_to_roll = re.compile("die_to_roll: (\d+)")
    re_dmg_modifier = re.compile("dmg_modifier: (\d+)")
    re_critical_dmg = re.compile("critical_dmg: (\d+)")
    re_critical_range = re.compile("critical_range: (\d+)")
    re_range_increment = re.compile("range_increment: (\d+)")
    re_base_cost = re.compile("base_cost: (\d+)")
    re_weapon_category = re.compile("weapon_category: (\w+)")
    re_melee = re.compile("melee: (\w+)")
    re_weapon_type = re.compile("weapon_type: (\w+)")
    re_dmg_type = re.compile("dmg_type: (.+)")
    re_size = re.compile("size: (\w+)")
    re_reach = re.compile("reach: (\w+)")
    re_two_handed = re.compile("two_handed: (\w+)")
    # armour
    re_armour_bonus = re.compile("armour_bonus: (\d+)")
    re_max_dex_bonus = re.compile("max_dex_bonus: (\d+)")
    re_armour_check_penalty = re.compile("armour_check_penalty: (\d+)")
    re_arcane_spell_fail = re.compile("arcane_spell_fail: (\d+)")
    re_speed = re.compile("speed: \((\d+), (\d+)\)")
    re_shield = re.compile("shield: (\w+)")
    re_armour_type = re.compile("armour_type: (\w+)")
    # living
    re_mp = re.compile("mp: ([-0-9]+)/([-0-9]+)")
    re_status_msgs = re.compile("status_msgs: (.*)")
    re_vision_range = re.compile("vision_range: (\d+)")
    re_level = re.compile("level: (\d+)")
    re_hit_dice = re.compile("hit_dice: (.*)")
    re_race = re.compile("race: (.*)")
    re_ability_scores = re.compile(
        "str: (\d+) dex: (\d+) wis: (\d+) con: (\d+) int: (\d+) cha: (\d+)")

    types_of_entities = {
        "entity": model.entity.Entity,
        "weapon": model.entity.Weapon,
        "armour": model.entity.Armour,
        "living": model.entity.Living,
        "player": model.entity.Player,
    }

    entities = {}
    max_uid = 0

    with open(file_name, "r") as f:

        new_ent = None
        for line in f.readlines():
            # type: ... should be at the beginning for each entity
            result = re_type.match(line)
            if result:
                # figure out what type of an entity object to instantiate
                entity_type = result.group(1)
                new_ent = types_of_entities[entity_type]()
            if "-" == line[0]:
                entities[new_ent.name.lower()] = new_ent
                continue
            # basic
            result = re_uid.match(line)
            if result:
                new_ent.uid = int(result.group(1))
                if new_ent.uid > max_uid:
                    max_uid = new_ent.uid
                continue
            result = re_name.match(line)
            if result:
                new_ent.name = result.group(1)
                continue
            result = re_symbol.match(line)
            if result:
                new_ent.symbol = result.group(1)
                continue
            result = re_cur_loc.match(line)
            if result:
                new_ent.cur_loc = (
                    int(result.group(1)), int(result.group(2)))
                continue
            result = re_hp.match(line)
            if result:
                new_ent.cur_hp = int(result.group(1))
                new_ent.max_hp = int(result.group(2))
                continue
            result = re_short_desc.match(line)
            if result:
                new_ent.short_desc = result.group(1)
                continue
            result = re_long_desc.match(line)
            if result:
                new_ent.long_desc = result.group(1)
                continue
            result = re_weight.match(line)
            if result:
                new_ent.weight = float(result.group(1))
                continue
            result = re_volume.match(line)
            if result:
                new_ent.volume = float(result.group(1))
                continue
            result = re_friction.match(line)
            if result:
                new_ent.friction = float(result.group(1))
                continue
            # weapon
            result = re_die_to_roll.match(line)
            if result:
                new_ent.die_to_roll = int(result.group(1))
                continue
            result = re_dmg_modifier.match(line)
            if result:
                new_ent.dmg_modifier = int(result.group(1))
                continue
            result = re_critical_range.match(line)
            if result:
                new_ent.critical_range = int(result.group(1))
                continue
            result = re_critical_dmg.match(line)
            if result:
                new_ent.critical_dmg = int(result.group(1))
                continue
            result = re_range_increment.match(line)
            if result:
                new_ent.range_increment = int(result.group(1))
                continue
            result = re_base_cost.match(line)
            if result:
                new_ent.base_cost = int(result.group(1))
                continue
            result = re_weapon_category.match(line)
            if result:
                new_ent.weapon_category = result.group(1)
                continue
            result = re_melee.match(line)
            if result:
                new_ent.melee = result.group(1)
                continue
            result = re_weapon_type.match(line)
            if result:
                new_ent.weapon_type = result.group(1)
                continue
            result = re_dmg_type.match(line)
            if result:
                new_ent.dmg_type = result.group(1)
                continue
            result = re_size.match(line)
            if result:
                new_ent.size = result.group(1)
                continue
            result = re_reach.match(line)
            if result:
                new_ent.reach = result.group(1)
                continue
            result = re_two_handed.match(line)
            if result:
                new_ent.two_handed = result.group(1)
                continue
            # armour
            result = re_armour_bonus.match(line)
            if result:
                new_ent.armour_bonus = int(result.group(1))
                continue
            result = re_max_dex_bonus.match(line)
            if result:
                new_ent.max_dex_bonus = int(result.group(1))
                continue
            result = re_armour_check_penalty.match(line)
            if result:
                new_ent.armour_check_penalty = int(result.group(1))
                continue
            result = re_arcane_spell_fail.match(line)
            if result:
                new_ent.armour_spell_fail = int(result.group(1))
                continue
            result = re_speed.match(line)
            if result:
                new_ent.speed = (
                    int(result.group(1)), int(result.group(2)))
                continue
            result = re_shield.match(line)
            if result:
                new_ent.shield = result.group(1)
                continue
            result = re_armour_type.match(line)
            if result:
                new_ent.armour_type = result.group(1)
                continue
            # living
            result = re_mp.match(line)
            if result:
                new_ent.cur_mp = int(result.group(1))
                new_ent.max_mp = int(result.group(2))
                continue
            result = re_status_msgs.match(line)
            if result:
                new_ent.status_msgs = result.group(1).split(",")
                continue
            result = re_vision_range.match(line)
            if result:
                new_ent.vision_range = int(result.group(1))
                continue
            result = re_level.match(line)
            if result:
                new_ent.level = int(result.group(1))
                continue
            result = re_hit_dice.match(line)
            if result:
                new_ent.hit_dice = result.group(1)
                continue
            result = re_race.match(line)
            if result:
                new_ent.race = result.group(1)
                continue
            result = re_ability_scores.match(line)
            if result:
                new_ent.str = int(result.group(1))
                new_ent.dex = int(result.group(2))
                new_ent.wis = int(result.group(3))
                new_ent.con = int(result.group(4))
                new_ent.int = int(result.group(5))
                new_ent.cha = int(result.group(6))
                continue
            # player doesn't have anything extra over living for now
    return (entities, max_uid)


if __name__ == '__main__':
    load_entities("../entities.txt")
