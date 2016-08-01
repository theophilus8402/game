#!/usr/bin/python3

from time import time

from model.entity.living.round_info import *
from model.entity.living.status_effects import *
from model.info import Status

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

