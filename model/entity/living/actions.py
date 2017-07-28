#!/usr/bin/python3

from random import choice
from time import time

from model.entity.living.equip import EqSlots
from model.entity.living.living import get_roll_possibilities, determine_weapon_dmg
from model.entity.living.round_info import *
from model.entity.living.status_effects import *
from model.info import Status
from model.util import new_roll, RollType

def allowed_to_attack(entity):
    # This will check to see if the entity is allowed to attack this round
    #   for this particular round.  Does not check health status of entity
    #   such as being paralyzed or stunned.
    # Returns True if the action can be taken, False otherwise
    #   can be made.
    # I'm not going to worry about pauses between commands for now.  I will still
    #   be keeping track of rounds, however.

    info = entity.round_info
    take_action = True
    current_time = time()

    # check to see if we're starting a new round
    check_new_round(entity)

    if info.num_attacks >= entity.max_num_attacks:
        # exceeded the number of attacks limit
        return False

    if info.feet_moved > entity.speed:
        # moved farther than normal in a round
        return False

    if info.other_action == True:
        # entity has already done something else that precludes the ability to attack
        return False

    return take_action


def allowed_to_move(entity, distance=0):
    # This will check to see if the entity is allowed to move the given distance
    #   for this particular round.  Does not check health status of entity
    #   such as being paralyzed or stunned.

    info = entity.round_info
    take_action = True
    current_time = time()

    # check to see if we're starting a new round
    check_new_round(entity)

    if (info.feet_moved + distance) > entity.speed:
        # would move farther than normal
        #TODO: need to figure out stuff like charging and flying
        take_action = False

    return take_action


def entity_can_get_item(entity, item):
    status = Status.all_good
    # make sure entity can get the item this round
    if not round_info_can_interact_obj(entity):
        status = Status.cant_do_this_round
        return status

    # make sure the entity isn't afflicted with an impediment
    right_arm = check_health(entity, {Body.right_arm})
    left_arm = check_health(entity, {Body.left_arm})
    if right_arm and left_arm:
        status = Status.impeding_affliction
        return status, {right_arm, left_arm}

    # TODO: make sure there's enough room in the inventory
    # TODO: make sure the entity can pickup the extra weight
    return status


def hit(src_ent, dst_ent, eqslot):
    """
    At this point, we will assume the src_ent is capable of hitting the dst_ent.
    Will determine if the eqslot is valid.
    Determine attack/defence possibilities.
    Roll.
    Determine and apply damage if appropriate.
    """
    # determine if the eqslot is valid
    if eqslot not in {EqSlots.left_hand, EqSlots.right_hand,
        EqSlots.left_leg, EqSlots.right_leg}:
        return Status.invalid_eqslot

    # TODO: provide some amount of exp for even trying to hit
    # this should be a relatively small amount of exp
    # and, we might do exp for a particular branch of skills like physical combat

    # determine attack possibilities
    possibilities = get_roll_possibilities(src_ent, eqslot=eqslot)

    # determine defence possibilities
    possibilities.update(get_roll_possibilities(dst_ent, defence=True))

    # determine level of success
    roll_result, roll_num = new_roll(possibilities)

    # determine initial damage if any amount of success
    if roll_result in {RollType.hit, RollType.block, RollType.critical_hit}:
        attacking_item = src_ent.equipment[eqslot]
        dmg_info = determine_weapon_dmg(src_ent, attacking_item)

        # check if attack was blocked
        if roll_result is RollType.block:
            # determine the item that blocked the attack
            blocking_items = dst_ent.equipment.get_blocking_items()
            blocking_item = choice(blocking_items)

            # figure out how much to reduce the dmg
            block_amt = get_block_value(blocking_item)
            dmg_info.add_block(blocking_item, block_amt)

        # apply damage
        # TODO: I should apply damage here, but I shouldn't give it a total.
        #   I should give it a DmgInfo object.  That way, any method of giving
        #   dmg can be handled by the entity, and I don't have to duplicate the
        #   checking for resists.  Just let the entity check it's own resists
        applied_dmg = dst_ent.apply_damage(dmg_info)
        dmg_info.applied_dmg = applied_dmg

        # determine if target is still alive
        # TODO: or have something else check this?

    else:
        dmg_info = None
    
    return roll_result, roll_num, dmg_info

