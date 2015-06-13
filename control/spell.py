import model.spell
import control.socks
import control.entity

def show_entity_info(entity):
    if (entity.type == "living") or (entity.type == "player"):
        entity.send_msg("Name: {} hp: {}/{} mp: {}/{}".format(
            entity.name, entity.cur_hp, entity.max_hp, entity.cur_mp,
            entity.max_mp))
    else:
        entity.send_msg("Name: {} hp: {}/{}".format(entity.name,
            entity.cur_hp, entity.max_hp))


def show_spell_info(entity, spell):
    entity.send_msg("Spell name: {} change_hp: {} change_mp: {}".format(
        spell.name, spell.hp_change, spell.mp_change))


def cast_simple(spell, world, caster, target):
    show_entity_info(caster)
    show_entity_info(target)
    show_spell_info(caster, spell)

    can_cast = True

    """
    check requirements
    """
    # make sure caster has enough mana
    if ((caster.cur_mp + spell.mp_change) < 0):
        can_cast = False
        caster.send_msg("You don't have enough mana!")
    # check the requirements of the spell
    if "living" in spell.requirements:
        can_cast = (target.type == "living") or (target.type == "player")

    """
    cast spell
    """
    if can_cast:
        target.change_hp(caster, spell.hp_change)
        caster.change_mp(spell.mp_change)
        caster.send_msg(spell.msg.format(target=target.name))

        show_entity_info(caster)
        show_entity_info(target)


spells = {}


resurrection = model.spell.Spell()
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
    show_entity_info(caster)
    show_entity_info(target)
    show_spell_info(caster, spell)

    can_cast = True

    """
    check requirements:
    """
    # make sure the caster has enough mp
    if (caster.cur_mp + spell.mp_change) < 0:
        can_cast = False
        caster.send_msg("You don't have enough mana!")
    #TODO: check to make sure he's dead

    """
    cast spell
    """
    if can_cast:
        target.change_hp(caster, spell.hp_change)
        caster.change_mp(spell.mp_change)
        caster.send_msg(spell.msg.format(target=target.name))

        # move him back to the realm of the living
        #possible_coord_changes = [(0, 1), (1, 1), (1, 0), (1, -1), 
        #TODO: make it more centered on where the caster or the body is
        control.move.move(world, target, target.cur_loc, (1, 1))

        #TODO: change target's status effect so he is no longer dead

        show_entity_info(caster)
        show_entity_info(target)
resurrection.cast = cast_resurrection
spells["resurrection"] = resurrection


def initialize_spells(simple_spells):
    for spell in simple_spells:
        spell.cast = cast_simple
        spells[spell.name] = spell
    return spells


