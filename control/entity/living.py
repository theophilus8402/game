import model.entity.living

from model.entity.living import *
from model.entity.entity import *
from model.util import find_distance

#from view.errors import display_error_msg

ERROR_ATTACK_MISSED = 6

def action_hit(world, msg):
    """
    There will be two command words that can cause this function to be
    called: hit and fhit.  "hit" will only hit the target once.  "fhit"
    will cause the attacker to do a full round attack.  I'm doing it this
    way so that I don't have to keep on running the tests/checks each time
    the attacker wants to hit someone in a round.
    """

    status = 0
    src_ent = msg.src_entity
    status_msg_info = {
        "src_ent": src_ent,
    }


    words = msg.msg.split()
    if len(words) == 2:         # make sure it's only two words
        target_name = words[1]
        dst_ent = world.find_entity(target_name) # make sure target exists
        if not dst_ent:
            status = ERROR_TARGET_DOESNT_EXIST
        status_msg_info["dst_ent_name"] = target_name
    else:
        print("incorrect syntax: words : {}".format(words))
        status = ERROR_INCORRECT_SYNTAX

    if status == 0:     # make sure he's within a distance of 1 space
        nearby = (1 >= find_distance(src_ent.cur_loc, dst_ent.cur_loc))
        if not nearby:
            status = ERROR_TARGET_TOO_FAR

    if status == 0:     # check to make sure he can do the attack
        bad_status_msgs = check_status_msgs(src_ent, {PARALYZED,
            BROKEN_ARM})
        if len(bad_status_msgs) > 0:
            status = ERRORS_STATUS[bad_status_msgs.pop()]
        #TODO: need to figure out how to determine if the attacker has
        # enough action points for the round to do the attack."

    if status == 0:     # conduct the attack
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
                status = ERROR_ATTACK_MISSED
            if status == 0:     # you hit!
                dmg = determine_weapon_dmg(src_ent, dst_ent)
                attack_msg_info["dmg"] = dmg
                attack_msg_info["weapon"] = dst_ent.eq["right_hand"] #TODO
                result = change_hp(dst_ent, dmg)
                #display_attacker_info(src_ent, attack_msg_info)
                #display_defender_info(dst_ent, attack_msg_info)
            if result == KILLED_TARGET:
                #TODO: do something about killing a target.
                break

    src_ent.comms.send("status: {}".format(status))
    return status
