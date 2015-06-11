#!/usr/bin/python3.4

import control.socks

"""
This function can be used to heal or dmg a target.
hp_change can be positive to heal someone or negative to hurt someone
If the dst_entity dies, we will give exp to the src_entity and kill
the dst_entity.
"""
def change_hp_entity(world, src_entity, dst_entity, hp_change):
    dst_entity.cur_hp = dst_entity.cur_hp - hp_change
    if dst_entity.cur_hp <= 0:
        control.socks.send_msg(world, src_entity,
            "You killed {}!".format(src_entity.name))
        control.mymap.kill_creature(world, src_entity, dst_entity)


