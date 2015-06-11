#!/usr/bin/python3.4

import re
import model.tile
import model.spells

def save_tiles(tiles, file_name):
    with open(file_name, "w") as f:
        for tile_index in tiles.keys():
            tile = tiles[tile_index]
            f.write("uid: {}\n".format(tile.uid))
            entity_uids = []
            for entity in tile.entities:
                entity_uids.append(str(entity.uid))
            f.write("entities: {}\n".format(",".join(entity_uids)))
            f.write("ground: {}\n".format(tile.ground))
            f.write("coord: {}\n".format(tile.coord))
            f.write("default_symbol: {}\n".format(tile.default_symbol))
            f.write("----------------------------\n");
    return True


def load_tiles(file_name):
    re_uid = re.compile("uid: (\d+)")
    re_entities = re.compile("entities: ([0-9,]*)")
    re_ground = re.compile("ground: (\w*)")
    re_coord = re.compile("coord: \(([-0-9]+), ([-0-9]+)\)")
    re_default_symbol = re.compile("default_symbol: (.)")

    tiles = {}
    max_uid = 0
    with open(file_name, "r") as f:
        new_tile = model.tile.Tile()
        for line in f.readlines():
            if "-" == line[0]:
                tiles[new_tile.coord] = new_tile
                new_tile = model.tile.Tile()
                #print("------------------")
                continue
            result = re_uid.match(line)
            if result:
                new_tile.uid = int(result.group(1))
                #print("uid: {}".format(new_tile.uid))
                if new_tile.uid > max_uid:
                    max_uid = new_tile.uid
                continue
            result = re_entities.match(line)
            if result:
                entity_uids = result.group(1).split(",")
                #print("entities: {}".format(entity_uids))
                continue
            result = re_ground.match(line)
            if result:
                new_tile.ground = result.group(1)
                #print("ground: {}".format(new_tile.ground))
                continue
            result = re_coord.match(line)
            if result:
                new_tile.coord = (int(result.group(1)), int(result.group(2)))
                #print("coord: {}".format(new_tile.coord))
                continue
            result = re_default_symbol.match(line)
            if result:
                new_tile.default_symbol = result.group(1)
                #print("default_symbol: {}".format(new_tile.default_symbol))
                continue
    return (tiles, max_uid)


def save_entities(entities, file_name):

    with open(file_name, "w") as f:
        for entity in entities:
            f.write("uid: {}\n".format(entity.uid))
            f.write("name: {}\n".format(entity.name))
            f.write("symbol: {}\n".format(entity.symbol))
            f.write("cur_loc: {}\n".format(entity.cur_loc))
            f.write("hp: {}/{}\n".format(entity.cur_hp, entity.max_hp))
            f.write("mp: {}/{}\n".format(entity.cur_mp, entity.max_mp))
            f.write("vision_range: {}\n".format(entity.vision_range))
            f.write("----------------------------\n");
    return True


def load_entities(file_name):

    re_uid = re.compile("uid: (\d+)")
    re_name = re.compile("name: (\w+)")
    re_symbol = re.compile("symbol: (.)")
    re_cur_loc = re.compile("cur_loc: \((\d+), (\d+)\)")
    re_hp = re.compile("hp: ([-0-9]+)/([-0-9]+)")
    re_mp = re.compile("mp: ([-0-9]+)/([-0-9]+)")
    re_vision_range = re.compile("vision_range: (\d+)")

    entities = []

    with open(file_name, "r") as f:

        new_ent = model.tile.Entity()
        for line in f.readlines():
            if "-" == line[0]:
                entities.append(new_ent)
                new_ent = model.tile.Entity()
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
                new_ent.cur_loc = (int(result.group(1)), int(result.group(2)))
                continue
            result = re_hp.match(line)
            if result:
                new_ent.cur_hp = int(result.group(1))
                new_ent.max_hp = int(result.group(2))
                continue
            result = re_mp.match(line)
            if result:
                new_ent.cur_mp = int(result.group(1))
                new_ent.max_mp = int(result.group(2))
                continue
            result = re_vision_range.match(line)
            if result:
                new_ent.vision_range = int(result.group(1))
                continue
    return entities


def load_spells(file_name):

    re_name = re.compile("name: (.*)")
    re_msg = re.compile("msg: (.*)")
    re_change_hp = re.compile("hp_change: ([-0-9]*)")
    re_mp_cost = re.compile("mp_change: ([-0-9]*)")
    re_recipient_status_effect = re.compile("recipient_status_effect: (.*)")
    re_status_effect_duration = re.compile("status_effect_duration: (.*)")
    re_cast_time = re.compile("cast_time: ([-0-9]*)")
    re_requirements = re.compile("requirements: (.*)")
    re_tile_effect = re.compile("tile_effect: (.*)")
    re_radius = re.compile("radius: (\d+)")
    re_area_type = re.compile("area_type: (.*)")

    spells = {}

    with open(file_name, "r") as f:

        new_spell = model.spells.Spell()
        for line in f.readlines():
            if "-" == line[0]:
                print("name: {}".format(new_spell.name))
                print("msg: {}".format(new_spell.msg))
                print("hp_change: {}".format(new_spell.hp_change))
                print("mp_change: {}".format(new_spell.mp_change))
                print("recipient_status_effect: {}".format(new_spell.recipient_status_effect))
                print("status_effect_duration: {}".format(new_spell.status_effect_duration))
                print("cast_time: {}".format(new_spell.cast_time))
                print("requirements: {}".format(new_spell.requirements))
                print("tile_effect: {}".format(new_spell.tile_effect))
                print("radius: {}".format(new_spell.radius))
                print("area_type: {}".format(new_spell.area_type))
                print("---------------------")
                """
                """
                spells[new_spell.name] = new_spell
                new_spell = model.spells.Spell()
                continue
            result = re_name.match(line)
            if result:
                new_spell.name = result.group(1).strip()
                continue
            result = re_msg.match(line)
            if result:
                new_spell.msg = result.group(1).strip()
                continue
            result = re_change_hp.match(line)
            if result:
                try:
                    new_spell.hp_change = int(result.group(1))
                except:
                    pass
                continue
            result = re_mp_cost.match(line)
            if result:
                try:
                    new_spell.mp_change = int(result.group(1))
                except:
                    pass
                continue
            result = re_recipient_status_effect.match(line)
            if result:
                new_spell.recipient_status_effect = result.group(1).strip()
                continue
            result = re_status_effect_duration.match(line)
            if result:
                try:
                    new_spell.status_effect_duration = int(result.group(1))
                except:
                    pass
                continue
            result = re_cast_time.match(line)
            if result:
                try:
                    new_spell.cast_time = int(result.group(1))
                except:
                    pass
                continue
            result = re_requirements.match(line)
            if result:
                new_spell.requirements = result.group(1).strip()
                continue
            result = re_tile_effect.match(line)
            if result:
                new_spell.tile_effect = result.group(1).strip()
                continue
            result = re_radius.match(line)
            if result:
                try:
                    new_spell.radius = int(result.group(1))
                except:
                    pass
                continue
            result = re_area_type.match(line)
            if result:
                new_spell.area_type = result.group(1).strip()
    return spells


if __name__ == '__main__':
    load_entities("../entities.txt")
