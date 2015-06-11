import model.spells
import control.socks
import control.entities

def show_entity_info(world, entity):
    control.socks.send_msg(world, entity,
        "Name: {} hp: {}/{} mp: {}/{}".format(
        entity.name, entity.cur_hp, entity.max_hp, entity.cur_mp,
        entity.max_mp))


def show_spell_info(world, entity, spell):
    control.socks.send_msg(world, entity,
        "Spell name: {} change_hp: {} change_mp: {}".format(
        spell.name, spell.hp_change, spell.mp_change))


def cast_simple(spell, world, caster, target):
    show_entity_info(world, caster)
    show_entity_info(world, target)

    show_spell_info(world, caster, spell)
    control.entities.change_hp_entity(world, caster, target, spell.hp_change)
    caster.cur_mp = caster.cur_mp + spell.mp_change
    control.socks.send_msg(world, caster, spell.msg.format(target=target.name))

    show_entity_info(world, caster)
    show_entity_info(world, target)


spells = {}


resurrection = model.spells.Spell()
resurrection.name = "resurrection"
resurrection.msg = "You waggle your fingers near your temples and accidentally resurrect {target}!"
resurrection.hp_change = 4
resurrection.mp_change = -8
resurrection.recipient_status_effect = None
resurrection.status_effect_duration = None
resurrection.cast_time = 3
resurrection.requirements = "hands"
resurrection.tile_effect = None
resurrection.radius = 1
resurrection.area_type = "circle"
def cast_resurrection(spell, world, caster, target):
    show_entity_info(world, caster)
    show_entity_info(world, target)
    show_spell_info(world, caster, spell)

    control.entities.change_hp_entity(world, caster, target, spell.hp_change)
    caster.cur_mp = caster.cur_mp + spell.mp_change
    control.socks.send_msg(world, caster, spell.msg.format(target=target.name))

    # move him back to the realm of the living
    #possible_coord_changes = [(0, 1), (1, 1), (1, 0), (1, -1), 
    #TODO: make it more centered on where the caster or the body is
    control.move.move(world, target, target.cur_loc, (1, 1))

    #TODO: change target's status effect so he is no longer dead

    show_entity_info(world, caster)
    show_entity_info(world, target)
resurrection.cast = cast_resurrection
spells["resurrection"] = resurrection


def initialize_spells(simple_spells):
    for spell in simple_spells:
        spell.cast = cast_simple
        spells[spell.name] = spell
    return spells


