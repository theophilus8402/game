import collections

import control.mymap
from model.entity.basic_entity import change_hp
from model.entity.living.living import *
from model.entity.living.actions import *
from model.entity.living.equip import *
from control.entity.blob import handle_blob_input
from control.entity.send_msg import format_and_send_msg, send_error_msg
from model.entity.inventory import *
from model.entity.living.status_effects import *
from model.entity.util import *
from model.info import Status, get_dir_word
from model.map import direction_coords
from model.msg import ActionMsgs
from model.world import get_tile, move_entity, entities_within_distance
from model.tile import tile_get_entity, tile_remove_entity
from model.util import distance_between_coords, roll
from view.msgs.basic import MsgType


def handle_action_msgs(world):
    continue_loop = True
    msg_queue = world.immediate_action_msgs
    while not msg_queue.empty():
        msg = msg_queue.get()
        msg_text = msg.msg
        entity = msg.src_entity
        if msg_text == "exit" and entity_has_status_effect(entity,
            Blessings.game_master):
            continue_loop = False
            entity.comms.send("Goodbye!  We'll miss you!")
        elif getattr(entity, "blob_state", False):
            handle_blob_input(world, msg)
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
    msg_info["dir"] = direction
    if not direction:
        status = Status.incorrect_syntax
        send_error_msg(msg_info, status)
        return status

    if not allowed_to_move(entity, distance=5):
        status = Status.cant_do_this_round
        send_error_msg(msg_info, status)
        return status

    #TODO: Make sure we can move into the room
    delta_coord = directioin_coords[direction]
    dst_coord = entity.coord + delta_coord

    right_leg_aff = check_health(entity, {Body.right_leg})
    left_leg_aff = check_health(entity, {Body.left_leg})
    if right_leg_aff and left_leg_aff:
        # TODO cannot move
        msg_info["afflictions"] = {right_leg_aff, left_leg_aff}
        status = Status.impeding_affliction
        send_error_msg(msg_info, status)
        return status
    elif right_leg_aff or left_leg_aff:
        affliction = right_leg_aff if right_leg_aff else left_leg_aff
        msg_info["afflictions"] = {right_leg_aff, left_leg_aff}
        # should force entity to hobble

    status = move_entity(world, entity, dst_coord)
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

    # check the appropriate arm/hand to see if it's healthy enough to attack
    hand_to_use = entity.main_hand
    required_parts = {hand_to_use}
    affliction = check_health(entity, required_parts)
    if affliction:
        status = Status.impeding_affliction
        msg_info["afflictions"] = {affliction}
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


def action_look_here(world, msg):
    entity = msg.src_entity
    cur_tile = get_tile(world, entity.coord)
    status = Status.all_good

    msg_info = {}
    msg_info["msg_type"] = MsgType.action_look_here
    msg_info["actor"] = entity
    tile_entities = [ent for ent in cur_tile.entities if ent != entity]
    msg_info["tile_entities"] = tile_entities
    msg_info["entities"] = [entity]

    sight_aff = check_health(entity, {Body.eyes})
    if sight_aff:
        status = Status.impeding_affliction
        msg_info["afflictions"] = {sight_aff}
        send_error_msg(msg_info, Status.impeding_affliction)
    else:
        format_and_send_msg(msg_info)
    return status


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


def action_get(world, msg):
    entity = msg.src_entity
    words = msg.msg.split()
    status = Status.all_good

    entities_nearby = list(entity.peeps_nearby) + [entity]

    msg_info = {
        "msg_type"  :   MsgType.action_get,
        "actor"     :   entity,
        "recipients":   [],
        "entities"  :   entities_nearby,
        }

    # make sure the entity specified an item
    if len(words) == 1:
        status = Status.getting_nothing
        send_error_msg(msg_info, status)
        return status

    # make sure the item exists and is in the same tile as the entity
    name = " ".join(words[1:])
    tile = get_tile(world, entity.coord)
    item = tile_get_entity(tile, name)
    msg_info["item"] = item
    if item == Status.target_doesnt_exist:
        status = item
        send_error_msg(msg_info, status)
        return status

    # make sure the entity can get the item
    status = entity_can_get_item(entity, item)
    if status != Status.all_good:
        if isinstance(status, tuple):
            status, afflictions = status
            msg_info["afflictions"] = afflictions
        send_error_msg(msg_info, status)
        return status

    # get the item
    tile_remove_entity(tile, item)
    inventory_add_item(entity.inventory, item)
    # TODO: test for return code??

    # set the flag in the round info
    round_info_entity_interacted_w_obj(entity)

    format_and_send_msg(msg_info)

    return status


def action_wear(world, msg):
    entity = msg.src_entity
    words = msg.msg.split()
    status = Status.all_good
    cmd_word = words[0]

    entities_nearby = list(entity.peeps_nearby) + [entity]
    if cmd_word == "wear" or cmd_word == "equip":
        msg_type = MsgType.action_wear
    else:
        msg_type = MsgType.action_wield
    msg_info = {
        "msg_type"  :   msg_type,
        "actor"     :   entity,
        "recipients":   [],
        "entities"  :   entities_nearby,
        }

    # example syntax:
    # wield short sword
    # wield right short sword
    # wield left shield
    # equip armour
    # wear shirt
    # wear right ring
    side = None
    if (len(words) > 2) and (words[1] in ["right", "left"]):
        # correct syntax and specified a side
        side = words[1]
        item_name = " ".join(words[2:])
    elif (len(words) > 1) and (words[1] not in ["right", "left"]):
        # correct syntax and did not specify a side
        item_name = " ".join(words[1:])
    else:
        # incorrect syntax
        status = Status.incorrect_syntax
        send_error_msg(msg_info, status)
        return status

    # find the item in the inventory
    inv = entity.inventory
    item = inventory_find_item(inv, item_name)
    if not item:
        status = Status.item_not_in_inventory
        msg_info["item_name"] = item_name
        send_error_msg(msg_info, status)
        return status

    # determine the equipment slot
    eq_slot = determine_eq_slot(entity, item, side)
    if ((side and item.eq_slot not in [EqSlots.hand, EqSlots.ring_finger]) or 
        (cmd_word == "wield" and item.eq_slot is not EqSlots.hand) or
        (cmd_word in ["equip", "wear"] and item.eq_slot is EqSlots.hand)):
        # basically, you wields stuff in your hands and wear/equip stuff elsewhere
        status = Status.incorrect_syntax
        send_error_msg(msg_info, status)
        return status
    if not eq_slot:
        status = Status.equipment_slot_not_free
        send_error_msg(msg_info, status)
        return status

    # equip the item
    status = entity_equip_item(entity, item, eq_slot)
    if status != Status.all_good:
        send_error_msg(msg_info, status)

    msg_info["item"] = item
    msg_info["eq_slot"] = eq_slot
    format_and_send_msg(msg_info)

    return status


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
default_world_actions["get"] = action_get
default_world_actions["lh"] = action_look_here
default_world_actions["say"] = action_say
default_world_actions["wear"] = action_wear
default_world_actions["wield"] = action_wear
default_world_actions["equip"] = action_wear

