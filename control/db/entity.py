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

def save_all_entities(entities, file_name):
    with open(file_name, "w") as f:
        for entity_name in entities:
            entity = entities[entity_name]
            save_entity(entity, f)
            f.write("-------------------\n")

"""
Future saving entity stuff:
            f.write("mp: {}/{}\n".format(entity.cur_mp, entity.max_mp))
            f.write("vision_range: {}\n".format(entity.vision_range))

Future loading entity stuff
    re_mp = re.compile("mp: ([-0-9]+)/([-0-9]+)")
    re_vision_range = re.compile("vision_range: (\d+)")

            result = re_mp.match(line)
            if result:
                new_ent.cur_mp = int(result.group(1))
                new_ent.max_mp = int(result.group(2))
                continue
            result = re_vision_range.match(line)
            if result:
                new_ent.vision_range = int(result.group(1))
                continue
"""

def load_entities(file_name):

    re_type = re.compile("type: (\w+)")
    re_uid = re.compile("uid: (\d+)")
    re_name = re.compile("name: (\w+)")
    re_symbol = re.compile("symbol: (.)")
    re_cur_loc = re.compile("cur_loc: \((\d+), (\d+)\)")
    re_hp = re.compile("hp: ([-0-9]+)/([-0-9]+)")
    re_short_desc = re.compile("short_desc: (.+)")
    re_long_desc = re.compile("long_desc: (.+)")
    re_weight = re.compile("weight: ([.0-9]+)")
    re_volume = re.compile("volume: ([.0-9]+)")
    re_friction = re.compile("friction: ([.0-9]+)")

    types_of_entities = {
        "entity": model.entity.Entity,
        #"weapon": model.entity.Weapon,
        #"armour": model.entity.Armour,
        #"living": model.entity.Living,
        #"player": model.entity.Player,
    }

    entities = {}

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
            result = re_uid.match(line)
            if result:
                new_ent.uid = int(result.group(1))
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
    return entities


if __name__ == '__main__':
    load_entities("../entities.txt")
