import collections

import control.mymap
from model.entity.entity import *
from model.entity.living import *
from model.entity.status_effects import *
from model.entity.util import *
from model.info import dir_coord_changes, Status
from model.msg import ActionMsgs
import model.world
from model.util import distance_between_coords, roll
from view.msgs import *


def get_input_from_entities(world, readable):
    for s in readable:
        entity = world.socket_entity_map[s]
        data = entity.comms.recv()
        if data:
            command = data.split()[0]
            if command in entity.known_cmds:
                new_msg = ActionMsgs(cmd_word=command,
                    msg=data, src_entity=entity)
                world.immediate_action_msgs.put(new_msg)
            else:
                entity.comms.send("Huh? What is {}".format(command))


def handle_action_msgs(world):
    continue_loop = True
    msg_queue = world.immediate_action_msgs
    while not msg_queue.empty():
        msg = msg_queue.get()
        msg_text = msg.msg
        src_ent = msg.src_entity
        if msg_text == "exit":
            continue_loop = False
            src_ent.comms.send("Goodbye!  We'll miss you!")
        else:
            action = world.actions[msg.cmd_word]
            action(world, msg)
        #src_ent.comms.send(msg)     # this just shows what msg was sent
    return continue_loop


def run_ai(world):
    for ai in world.ai_entities:
        ai.run()


def default_action(world, msg):
    msg.src_entity.comms.send("Unknown world action: \"{}\"?".format(msg.msg))


def action_move(world, msg):


    status = Status.all_good
    entity = msg.src_entity
    entities_nearby = list(entity.peeps_nearby) + [entity]
    msg_info = {
        "msg_type"  :   MsgType.action_move,
        "actor"     :   entity,
        "recipients":   [],
        "entities"  :   entities_nearby,
        }

    words = msg.msg.split()

    if len(words) != 1:
        status = Status.incorrect_syntax
        send_error_msg(msg_info, status)
        return status

    direction = get_dir_word(words[0])
    msg_info["direction"] = direction
    if not direction:
        status = Status.incorrect_syntax
        send_error_msg(msg_info, status)
        return status

    if not allowed_to_move(entity, distance=5):
        status = Status.cant_do_this_round
        send_error_msg(msg_info, status)
        return status

    #TODO: Make sure we can move into the room
    delta_coord = dir_coord_changes[direction]
    dst_coord = src_ent.coord + delta_coord

    right_leg_aff = check_health(entity, Body.right_leg)
    left_leg_aff = check_health(entity, Body.left_leg)
    if right_leg and left_leg:
        # TODO cannot move
        msg_info["afflictions"] = {right_leg_aff, left_leg_aff}
        status = Status.impeding_affliction
        send_error_msg(msg_info, status)
        return status
    elif right_leg_aff or left_leg_aff:
        affliction = right_leg_aff if right_leg_aff else left_leg_aff
        msg_info["afflictions"] = {right_leg_aff, left_leg_aff}
        # should force entity to hobble

    status = model.world.move_entity(world, entity, dst_coord)
    if status == Status.tile_doesnt_exist:
        send_error_msg(msg_info, status)
        return status
        
    format_and_send_msg(msg_info)
    return status


def action_look(world, msg):
    """
    TODO:
    In the future, I'd like to be able to look at something, but for now, let's focus
    on being able to view the map.
    """
    control.mymap.display_map(world, msg.src_entity)


# time defaults
#MOVE_WAIT = .3
#ATTACK_WAIT = 1
ROUND_LENGTH = 4

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
    if (current_time >= (info.time_started + ROUND_LENGTH)):
        # restart the round
        info = RoundInfo()
        entity.round_info = info

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
    if (current_time >= (info.time_started + ROUND_LENGTH)):
        # restart the round
        info = RoundInfo()

    if (info.feet_moved + distance) > entity.speed:
        # would move farther than normal
        #TODO: need to figure out stuff like charging and flying
        take_action = False

    return take_action


def send_error_msg(msg_info, error):
    msg_info["msg_type"] = MsgType.error
    msg_info["error_code"] = error
    msg_info["entities"] = [msg_info["actor"]]
    format_and_send_msg(msg_info)

def format_and_send_msg(msg_info):
    formatted_msgs = format_msg(msg_info)
    for entity, msg in formatted_msgs:
        entity.comms.send(msg)


def action_hit(world, msg):
    # Here's how I think I'm going to handle hitting stuff.
    # Considerations:
    #   simple attack with one weapon and one attack per round,
    #   attacking with one weapon multiple times per round,
    #   attacking with two weapons once per round, and
    #   attacking with two weapons multiple times per round.
    # Before getting two-weapon fighting to work, let's get one attack
    #   per round to work.  Then go to one weapon and multiple attacks.
    # The entity is going to keep track of rounds and number of moves and
    #   actions the entity has taken.  There will be something that checks
    #   to see if the entity is even allowed to make that action.
    # There's going to be some pause between actions.  For example:
    #   move 5ft pause .5 sec
    #   attack w/ one or both hands wait 1 sec
    #      (have to give time for the extra actions that are possible)
    # Numbers per round: speed: 30ft, attacks: 4
    #   30/5 = 6 moves      6moves * .3s/move = 1.8s
    #   4att * 1s/att = 4s
    # I can make move balance and attack balance separate. That way, they can
    #   move and attack immediately, but must wait for both the attack and
    #   the move balance to come back.

    status = Status.all_good
    entity = msg.src_entity
    entities_nearby = list(entity.peeps_nearby) + [entity]
    msg_info = {
        "msg_type"  :   MsgType.action_hit,
        "actor"     :   entity,
        "recipients":   [],
        "entities"  :   entities_nearby,
        }

    words = msg.msg.split()

    # make sure the entity hasn't taken too many actions this round
    if not allowed_to_attack(entity):
        status = Status.cant_do_this_round
        send_error_msg(msg_info, status)
        return status

    # make sure it's the correct syntax "hit target"
    if len(words) != 2:
        status = Status.incorrect_syntax
        send_error_msg(msg_info, Status.incorrect_syntax)
        return status

    target_name = words[1]
    target = world.find_entity(target_name)

    # make sure the entity exists and is not too far away
    if not target or distance_between_coords(entity.coord, target.coord) >= 1.5:
        # target doesn't exist
        status = Status.target_doesnt_exist
        send_error_msg(msg_info, Status.target_doesnt_exist)
        return status

    msg_info["recipients"] = [target]

    # check the apropriate arm/hand to see if it's healthy enough to attack
    hand_to_use = entity.main_hand
    required_parts = {hand_to_use}
    affliction = check_health(entity, required_parts)
    if affliction:
        status = Status.impeding_affliction
        msg_info["affliction"] = affliction
        send_error_msg(msg_info, Status.impeding_affliction)
        return status

    weapon = get_weapon_in_hand(entity, hand=hand_to_use)
    msg_info["weapon"] = weapon

    # TODO! Some afflictions may make the entity do something different like attack
    #   a random individual or just make fun of him/her

    # attack!
    attack_bonus = get_attack_bonus(entity, weapon, melee=True)
    attack_roll = roll(1, 20, attack_bonus)
    entity.round_info.num_attacks += 1
    if target.ac > attack_roll:
        status = Status.attack_missed
        send_error_msg(msg_info, Status.attack_missed)
        return status

    # calculate damage
    dmg = determine_weapon_dmg(entity, target)
    msg_info["dmg"] = dmg
    change_hp(target, dmg)
    if target.cur_hp <= 0:
        # target died!
        msg_info["status"] = Status.killed_target
        #TODO: do something about killing a target.
    format_and_send_msg(msg_info)

    return status

def entities_within_distance(center_coord, entities, distance):
    """
    Takes a center_coord, a list of entities, and a distance.
    It tests each entity to see if it's close enough to the center_coord.
    If so, the entity get's appended to a new list which is returned
    at the end of the function.  Defaults to sending an empty list.
    """
    ents_within_distance = []
    for entity in entities:
        if distance_between_coords(center_coord, entity.coord) <= distance:
            ents_within_distance.append(entity)
    return ents_within_distance

def action_say(world, msg):
    entity = msg.src_entity
    words = msg.msg.split()
    say_distance = 5
    dst_entity = None

    ents_within_say_dist = entities_within_distance(entity.coord, entity.peeps_nearby,
        say_distance)
    ents_within_say_dist.append(entity)

    msg_info = {
        "msg_type"  :   MsgType.action_say,
        "actor"     :   entity,
        "recipients":   [],
        "entities"  :   ents_within_say_dist,
        }

    if (len(words) > 2) and (words[1] == "to"):
        # direct a msg at someone in particular
        dst_entity_name = words[2]
        for tmp_entity in ents_within_say_dist:
            if tmp_entity.name.lower() == dst_entity_name.lower():
                # that entity exists and is nearby!
                dst_entity = tmp_entity
                break
        words_said = " ".join(words[3:])
        if not dst_entity:
            # entity was too far away or doesn't exist
            msg_info["msg_type"] = MsgType.error
            msg_info["error_code"] = Status.target_doesnt_exist
        else:
            msg_info["say_to"] = True
            msg_info["recipients"].append(dst_entity)
    else:
        # saying stuff to "everyone" in the area (within hearing range)
        words_said = " ".join(words[1:])

    if len(words_said) < 1:
        # user didn't specify any words after the "say" command
        msg_info["msg_type"] = MsgType.error
        msg_info["error_code"] = Status.saying_nothing
    else:
        msg_info["words"] = words_said[0].upper() + words_said[1:]

    format_and_send_msg(msg_info)


default_world_actions = collections.defaultdict(lambda: default_action)
default_world_actions["hit"] = action_hit
default_world_actions["n"] = action_move
default_world_actions["nw"] = action_move
default_world_actions["ne"] = action_move
default_world_actions["e"] = action_move
default_world_actions["s"] = action_move
default_world_actions["se"] = action_move
default_world_actions["sw"] = action_move
default_world_actions["w"] = action_move
default_world_actions["l"] = action_look
default_world_actions["look"] = action_look
default_world_actions["say"] = action_say

