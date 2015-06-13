#!/usr/bin/python3.4

import control.socks


def show_entity_info(world, entity):
    entity.send_msg("Name: {} hp: {}/{} mp: {}/{}".format(
        entity.name, entity.cur_hp, entity.max_hp, entity.cur_mp,
        entity.max_mp))


"""
This function can be used to heal or dmg a target.
hp_change can be positive to heal someone or negative to hurt someone
If the dst_entity dies, we will give exp to the src_entity and kill
the dst_entity.
"""
def change_hp_entity(world, src_entity, dst_entity, hp_change):
    
    #show_entity_info(world, dst_entity)
    dst_entity.cur_hp = dst_entity.cur_hp + hp_change
    #show_entity_info(world, dst_entity)
    if dst_entity.cur_hp <= 0:
        src_entity.send_msg("You killed {}!".format(src_entity.name))
        control.mymap.kill_creature(world, src_entity, dst_entity)


def show_spell_info(world, entity, spell):
    entity.send_msg("Spell name: {} change_hp: {} change_mp: {}".format(
        spell.name, spell.hp_change, spell.mp_change))


def cast_spell(world, src_entity, dst_entity, spell_name):
    
    show_entity_info(world, src_entity)
    show_entity_info(world, dst_entity)

    if spell_name in world.spells.keys():
        spell = world.spells[spell_name]

        show_spell_info(world, src_entity, spell)
        change_hp_entity(world, src_entity, dst_entity, spell.hp_change)
        src_entity.cur_mp  = src_entity.cur_mp + spell.mp_change
        src_entity.send_msg(spell.msg.format(target=dst_entity.name))

    show_entity_info(world, src_entity)
    show_entity_info(world, dst_entity)
