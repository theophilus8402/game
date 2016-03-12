import model.util


CMDS_BASIC_MOVEMENT = {"n", "ne", "e", "se", "s", "sw", "w", "nw"}
CMDS_BASIC_ATTACK = {"hit", "fhit", "cast"}
CMDS_BASIC_HUMANOID = {"get", "eat", "drink", "wear", "wield", "remove",
    "unwield", "l", "look", "quit", "exit"}
CMDS_DEBUG = {"dist"}

PARALYZED = "paralyzed"
BROKEN_ARM = "broken_arm"
ERROR_TARGET_DOESNT_EXIST = 2
ERROR_INCORRECT_SYNTAX = 1
ERROR_TARGET_TOO_FAR = 5
ERRORS_STATUS = {
    PARALYZED: 3,
    BROKEN_ARM: 4,
}

def add_status_msg(entity, msg):
    entity.status_msgs.add(msg)


def remove_status_msg(entity, msg):
    try:
        entity.status_msgs.remove(msg)
    except:
        pass    # I don't think I want to do anything...


def check_status_msgs(entity, bad_msgs):
    return entity.status_msgs.intersection(bad_msgs)


def get_attack_bonus(src_ent, melee=True, range_pen=0):
    """
    att_bonus = base_att_bonus + ability_mod + size_mod + misc
    we'll do the d20 roll somehwere else
    This will return a list of attack bonuses
    """

    if melee:
        attribute = "str"
    else:
        attribute = "dex"
    attrib, ability_mod = src_ent.attrib[attribute]

    size_mod = model.util.size_modifiers[src_ent.size]
    misc_attack_bonus, misc_list = src_ent.attack_bonus["misc"]

    attack_bonus_list = []
    for base_attack_bonus in src_ent.attack_bonus["base"]:
        # attack_bonus (melee) = base_attack_bonus + str_mod + size_mod
        attack_bonus = (base_attack_bonus + ability_mod + size_mod 
            + misc_attack_bonus)
        # attack_bonus (ranged) = base_attack_bonus + dex_mod + size_mod
        # + range_penalty
        if not melee:
            attack_bonus += range_pen

        attack_bonus_list.append(attack_bonus)

    return attack_bonus_list


def check_successful_attack(src_ent, dst_ent, info=None):
    #TODO: actually implement this
    return True

def determine_weapon_dmg(src_ent, dst_ent):
    """
    dmg will be returned as a negative number to indicate that health
    should be subtracted from target.
    """
    #TODO: actually implement this
    dmg = -6
    return dmg


def hit(world, src_ent, dst_ent, full_attack=False):
    status = 0

    bad_status_msgs = check_status_msgs(src_ent, {PARALYZED, BROKEN_ARM})
    if bad_status_msgs == set():    # he doesn't have any bad status msgs 
        src_ent.comms.send("Ok, you're clean to hit {}!".format(
            dst_ent.name))
    else:
        src_ent.comms.send("Here's what's wrong with you: {}".format(
            bad_status_msgs))
        status = ERRORS_STATUS[bad_status_msgs.pop()] # just return one
                                                      # bad status msg

    # attack roll
    attack_bonus_list = get_attack_bonus(src_ent, melee=True)
    if not full_attack:
        attack_bonus_list = attack_bonus_list[0:1]
    for attack_bonus in attack_bonus_list:
        d20 = model.roll.roll(1, 20)

    # dmg
    return status

