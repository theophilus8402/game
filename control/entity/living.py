
import control.mymap
from model.entity.living import *
from model.entity.entity import *
from model.info import dir_coord_changes, Status
import model.world
import model.tile
from model.util import distance_between_coords


def action_move(world, msg):

    src_ent = msg.src_entity
    words = msg.msg.split()

    if len(words) == 1:     # correct number of words
        direction = words[0]
        if direction in dir_coord_changes:  # a proper direction
            #TODO: Make sure we can move
            #TODO: Make sure we can move into the room
            delta_coord = dir_coord_changes[direction]
            dst_coord = src_ent.coord + delta_coord
            src_ent.comms.send("Moving {}...".format(direction))
            status = model.world.move_entity(world, src_ent, dst_coord)
            if status == Status.tile_doesnt_exist:
                src_ent.comms.send("Eeep! There's no tile there!")


def action_look(world, msg):
    """
    TODO:
    In the future, I'd like to be able to look at something, but for now, let's focus
    on being able to view the map.
    """
    control.mymap.display_map(world, msg.src_entity)


def action_hit(world, msg):
    """
    There will be two command words that can cause this function to be
    called: hit and fhit.  "hit" will only hit the target once.  "fhit"
    will cause the attacker to do a full round attack.  I'm doing it this
    way so that I don't have to keep on running the tests/checks each time
    the attacker wants to hit someone in a round.
    """

    status = Status.all_good
    src_ent = msg.src_entity
    status_msg_info = {
        "src_ent": src_ent,
    }


    words = msg.msg.split()
    if len(words) == 2:         # make sure it's only two words
        target_name = words[1]
        dst_ent = world.find_entity(target_name) # make sure target exists
        if not dst_ent:
            status = Status.target_doesnt_exist
        status_msg_info["dst_ent_name"] = target_name
    else:
        print("incorrect syntax: words : {}".format(words))
        status = Status.incorrect_syntax

    if status == Status.all_good:     # make sure he's within a distance of 1 space
        nearby = (1 >= distance_between_coords(src_ent.coord, dst_ent.coord))
        if not nearby:
            status = Status.target_too_far_away

    if status == Status.all_good:     # check to make sure he can do the attack
        required_parts = {Body.right_arm, Body.left_arm}
        affliction = check_health(src_ent, required_parts)
        if affliction:
            src_ent.comms.send(
                "Ack! Something is wrong with you ({})! So you can't hit...".format(
                affliction))
            status = Status.affliction_impeding
        # TODO: Figure out how to print out the bad status effect

    if status == Status.all_good:     # conduct the attack
        attack_bonus_list = get_attack_bonus(src_ent, melee=True)
        if msg.cmd_word == "hit":       # only doing the first attack bonus
            attack_bonus_list = attack_bonus_list[0:1]
        for attack_bonus in attack_bonus_list:
            attack_msg_info = {
                "dst_ent_name": dst_ent.name
            }
            successful_attack = check_successful_attack(src_ent, dst_ent,
                info=attack_msg_info)
            if not successful_attack:       # conduct attack_roll
                status = Status.attack_missed
            if status == Status.all_good:     # you hit!
                dmg = determine_weapon_dmg(src_ent, dst_ent)
                attack_msg_info["dmg"] = dmg
                attack_msg_info["weapon"] = dst_ent.eq["right_hand"] #TODO
                change_hp(dst_ent, dmg)
                #display_attacker_info(src_ent, attack_msg_info)
                #display_defender_info(dst_ent, attack_msg_info)
            if dst_ent.cur_hp <= 0:
                status = Status.killed_target
                #TODO: do something about killing a target.

    src_ent.comms.send("status: {}".format(status))
    return status
