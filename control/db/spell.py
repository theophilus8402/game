#!/usr/bin/python3.4

import re
import model.spell


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

    spells = []

    with open(file_name, "r") as f:

        new_spell = model.spell.Spell()
        for line in f.readlines():
            if "-" == line[0]:
                """
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
                spells.append(new_spell)
                new_spell = model.spell.Spell()
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
