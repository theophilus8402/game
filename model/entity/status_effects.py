#!python3

import enum

@enum.unique
class Body(enum.Enum):
    none = 0
    mouth = 1
    voice = 2
    head = 3
    right_arm = 4
    left_arm = 5
    right_leg = 6
    left_leg = 7
    torso = 8
    # we could do things like:
    #   clear_headed    (for stupid, cursed, dizzy?)


@enum.unique
class Afflictions(enum.Enum):
    paralysis = 1
    broken_left_leg = 2
    silenced = 3
    webbed = 4
    dead = 5
    stupid = 6
    lost_balance = 7


afflictions_map = {
    Afflictions.paralysis : {Body.right_arm, Body.left_arm, Body.right_leg,
        Body.left_leg, Body.head, Body.torso},
    Afflictions.broken_left_leg : {Body.left_leg},
    Afflictions.silenced : {Body.voice},
    Afflictions.webbed : {Body.right_leg, Body.left_leg},
    Afflictions.dead : {Body.mouth, Body.voice, Body.head, Body.right_arm,
        Body.left_arm, Body.right_leg, Body.left_leg, Body.torso},
    Afflictions.stupid : {Body.head},
    Afflictions.lost_balance : {Body.right_arm, Body.left_arm, Body.right_leg,
        Body.left_leg},
}


# tested
def add_status_effect(entity, effect):
    '''
    Adds the effect to the entity's set of status_effects.  There will
    be no duplicate effects.  These effects can be either good or bad (afflictions).
    '''
    entity.status_effects.add(effect)

# tested
def remove_status_effect(entity, effect):
    '''
    Removes the effect from the entity's set of status_effects.  If the
    effect is not in the entity's list, it will do nothing.
    '''
    entity.status_effects.discard(effect)


def check_health(entity, body_parts):
    '''
    Returns the status of the entity's body_part in question.  If the entity has one
    or more afflictions that affect that body_part, the first affliction (in the set)
    will be returned.
    '''
    status = None
    for affliction in entity.status_effects:
        affected_parts = afflictions_map.get(affliction)
        if affected_parts and affected_parts.intersection(body_parts):
            status = affliction
            break
    return status
