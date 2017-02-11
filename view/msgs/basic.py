
from collections import defaultdict
import enum
import random
import re

from view.info import ViewStatus
from model.entity.living.status_effects import Body, check_health, get_affliction_name
from model.entity.living.equip import get_eq_slot_name
from model.info import Status, get_dir_word


TAB = "    "


@enum.unique
class MsgType(enum.Enum):
    system = 0
    action_say = 1
    error = 2
    action_hit = 3
    action_move = 4
    action_say_to = 5
    action_look_here = 6
    action_get = 7
    action_wear = 8
    action_wield = 9


class ViewMsgManager():

    def __init__(self, view_msgs=None):
        if view_msgs:
            self.view_msgs = view_msgs
        else:
            self.view_msgs = []

    def add_msgs(self, view_msgs):
        self.view_msgs.extend(view_msgs)

    def get_unformatted_msg(self, actor, entity, recipient):
        """
        Returns the first UnformattedMsg that the entity is capable of "seeing".
        Checks to see if the entity is blind/deaf and checks the requirements of
        the msg.
        """
        deaf = check_health(entity, {Body.ears})
        blind = check_health(entity, {Body.eyes})

        for msg in self.view_msgs:
            if entity == actor:
                return msg
            if ((entity != recipient) and msg.only_for_recipient == True):
                continue
            if (deaf != None and msg.can_be_deaf == False):
                continue
            if (blind != None and msg.can_be_blind == False):
                continue
            return msg
        return None

    def format_msgs(self, info):
        actor = info.get("actor")
        recipient = info.get("recip")
        formatted_msgs = []
        for entity in info.get("entities"):
            unformatted_msg = self.get_unformatted_msg(actor, entity, recipient)
            if unformatted_msg:
                formatted_msgs.append(
                    (entity, unformatted_msg.format_msg(info, entity)))
        return formatted_msgs


class UnformattedMsg():

    # this will be used to look for "{actor}" and what not in the msg
    field_pattern = re.compile("\{(.*?)\}")

    def __init__(self, unf_msg_list, can_be_deaf=False, can_be_blind=False,
        only_for_recipient=False):
        self.msg_str_list = unf_msg_list
        self.fields = []
        for msg in unf_msg_list:
            self.fields.extend(self.field_pattern.findall(msg))
        self.can_be_deaf = can_be_deaf
        self.can_be_blind = can_be_blind
        self.only_for_recipient = only_for_recipient

    def format_msg(self, info, entity):
        formatted_fields = {}
        msg = random.choice(self.msg_str_list)
        for field in self.fields:
            formatted_fields[field] = format_map[field](info, entity)
        return msg.format(**formatted_fields)


def format_error_msg(msg_info):
    # Must return a list of (entity, msg) tuples
    code = msg_info["error_code"]
    entity = msg_info["actor"]
    formatted_msgs = error_code_msgs[code].format_msgs(msg_info)
    return formatted_msgs


def format_system_msg(msg_info):
    # Must return a list of (entity, msg) tuples
    entity = msg_info["actor"]
    msg = msg_info["msg"].format(**msg_info)
    return [(entity, msg)]


def format_actor_possessive(info, entity, capitalize=False):
    actor = info.get("actor")
    actor_str = ""
    if entity == actor:
        actor_str = "your"
    else:
        actor_str = "his" if actor.male else "her"
    return actor_str if not capitalize else actor_str.capitalize()


def format_affliction_str(info, entity):
    afflictions = info["afflictions"]
    aff_names = [get_affliction_name(aff) for aff in afflictions]
    if len(afflictions) == 1:
        return aff_names[0]

    aff_names[-1] = "and {}".format(aff_names[-1])
    if len(afflictions) == 2:
        return " ".join(aff_names)
    else:
        return ", ".join(aff_names)


def format_actor(info, entity, capitalize=False):
    actor = info.get("actor")
    if not actor or not entity:
        return None

    you = "You" if capitalize else "you"

    return you if entity == actor else actor.name#.capitalize()


def format_normal_action(info, entity, action):
    actor = info.get("actor")
    return action if entity == actor else "{}s".format(action)


def format_recipient(info, entity, capitalize=False, possessive=False):
    actor = info.get("actor")
    recipient = info.get("recip")
    recipient_str = ""
    if (entity == recipient) and (entity == actor):
        recipient_str = "yourself" if not possessive else "your"
    elif entity == recipient:
        recipient_str = "you" if not possessive else "your"
    elif actor == recipient:
        if recipient.male:
            recipient_str = "himself" if not possessive else "his"
        else:
            recipient_str = "herself" if not possessive else "her"
    else:
        if recipient.male:
            recipient_str = recipient.name if not possessive else "his"
        else:
            recipient_str = recipient.name if not possessive else "her"
    return recipient_str if not capitalize else recipient_str.capitalize()


def format_tile_entities(info, entity):
    tile_entities = info.get("tile_entities")
    if len(tile_entities) > 0:
        lines = ["{}{}".format(TAB, ent.name) for ent in tile_entities]
        return "\n".join(lines)
    else:
        return "{}Nothing.".format(TAB)


def format_item_name(info, entity, capitalize=False):
    item = info.get("item")
    item_name = info.get("item_name")
    name_str = ""

    if item:
        name_str = item.name
    elif item_name:
        name_str = item_name

    if name_str:
        if name_str[0].lower() in ["a", "e", "i", "o", "u"]:
            name_str = "an {}".format(name_str)
        else:
            name_str = "a {}".format(name_str)
        if capitalize == True:
            name_str = name_str.capitalize()
    return name_str


def format_words(info, entity):
    return info.get("words")


def format_eq_slot(info, entity):
    return get_eq_slot_name(info["eq_slot"])


def format_dir(info, entity):
    return get_dir_word(info["dir"])


format_map = {
    "actor" : format_actor,
    "Actor" : lambda info, entity: format_actor(info, entity, capitalize=True),
    "actor_poss" : format_actor_possessive,
    "Actor_poss" : lambda info, ent: format_actor_possessive(info, ent,
                        capitalize=True),
    "recip" : format_recipient,
    "Recip" : lambda info, ent: format_recipient(info, ent, capitalize=True),
    "recip_poss" : lambda info, ent: format_recipient(info, ent, possessive=False),
    "Recip_poss" : lambda info, ent: format_recipient(info, ent, capitalize=True,
                        possessive=True),
    "afflictions" : format_affliction_str,
    "tile_entities" : format_tile_entities,
    "action_move" : lambda info, entity: format_normal_action(info, entity, "move"),
    "action_skip" : lambda info, entity: format_normal_action(info, entity, "skip"),
    "action_say" : lambda info, entity: format_normal_action(info, entity, "say"),
    "action_hit" : lambda info, entity: format_normal_action(info, entity, "hit"),
    "action_get" : lambda info, entity: format_normal_action(info, entity, "get"),
    "action_wear" : lambda info, entity: format_normal_action(info, entity, "wear"),
    "action_wield" : lambda info, entity: format_normal_action(info, entity,"wield"),
    "item" : format_item_name,
    "item_name" : format_item_name,
    "Item_name" : lambda info, entity: format_item_name(info, entity, capitalize=True),
    "eq_slot" : format_eq_slot,
    "words" : format_words,
    "dir" : format_dir,
}


def format_action_msg(msg_info):
    msg_type = msg_info.get("msg_type")
    entities = msg_info.get("entities")
    actor = msg_info.get("actor")
    recipient = msg_info.get("recipients")
    if recipient:
        recipient = recipient[0]
        #TODO: allow for multiple recipients
        msg_info["recip"] = recipient
    formatted_msgs = view_msg_managers[msg_type].format_msgs(msg_info)
    return formatted_msgs


handle_msgs = defaultdict(lambda: format_action_msg)
handle_msgs[MsgType.system] = format_system_msg
handle_msgs[MsgType.error] = format_error_msg


action_say_msg_manager = ViewMsgManager([
    UnformattedMsg(["{Actor} {action_say}, '{words}'"]),
    UnformattedMsg([
        "You see {actor} moving {actor_poss} lips but can't hear anything."],
        can_be_deaf=True),
    UnformattedMsg(["You hear someone say, '{words}'"], can_be_blind=True),
    ])


action_say_to_msg_manager = ViewMsgManager([
    UnformattedMsg(["{Actor} {action_say} to {recip}, '{words}'"]),
    UnformattedMsg([
        "You see {actor} moving {actor_poss} lips but can't hear anything."],
        can_be_deaf=True),
    UnformattedMsg(["You hear someone say, '{words}'"], can_be_blind=True),
    ])
 
 
action_hit_msg_manager = ViewMsgManager([
    UnformattedMsg(["{Actor} maliciously {action_hit} {recip}!"], can_be_deaf=True),
    UnformattedMsg(["Someone hit you!"], can_be_deaf=True, can_be_blind=True,
        only_for_recipient=True),
    UnformattedMsg(["You hear some fighting going on nearby."], can_be_blind=True),
    UnformattedMsg(["Someone hit you!"], only_for_recipient=True),
    ])


action_move_msg_manager = ViewMsgManager([
    UnformattedMsg(["{Actor} {action_move} to the {dir}.",
                    "{Actor} {action_skip} to the {dir}."], can_be_deaf=True),
    UnformattedMsg(["You hear someone nearby move."], can_be_blind=True),
    ])


action_look_here_msg_manager = ViewMsgManager([
    UnformattedMsg(["You see the following:\n{tile_entities}"], can_be_deaf=True),
    UnformattedMsg(["You can't see anything because you are blind."],
        can_be_blind=True),
    ])


action_get_msg_manager = ViewMsgManager([
    UnformattedMsg(["{Actor} {action_get} {item} from the floor."], can_be_deaf=True,
        can_be_blind=True),
    ])


action_wear_msg_manager = ViewMsgManager([
    UnformattedMsg(["{Actor} {action_wear} {item} on {actor_poss} {eq_slot}."],
        can_be_deaf=True),
    UnformattedMsg(["{Actor} {action_wear} {item} on {actor_poss} {eq_slot}."],
        can_be_deaf=True, can_be_blind=True, only_for_recipient=True),
    ])


action_wield_msg_manager = ViewMsgManager([
    UnformattedMsg(["{Actor} {action_wield} {item} in {actor_poss} {eq_slot}."],
        can_be_deaf=True),
    UnformattedMsg(["{Actor} {action_wield} {item} in {actor_poss} {eq_slot}."],
        can_be_deaf=True, can_be_blind=True, only_for_recipient=True),
    ])


############### Error msg managers
error_code_msgs = {
    Status.saying_nothing : ViewMsgManager([
        UnformattedMsg(["Erm... you didn't actually say anything.",
        "Uh... you didn't say any words.  wanna try again?"], can_be_deaf=True,
        can_be_blind=True)
        ]),
    Status.target_doesnt_exist : ViewMsgManager([
        UnformattedMsg(["Either that entity doesn't exist or isn't close by.",
        "To whom are you referring?"], can_be_deaf=True, can_be_blind=True)
        ]),
    Status.cant_do_this_round : ViewMsgManager([
        UnformattedMsg(["You can't do that this round.",
        "Whoa there, slow down.  You need to wait until next turn."], can_be_deaf=True,
        can_be_blind=True)
        ]),
    Status.incorrect_syntax : ViewMsgManager([
        UnformattedMsg(["Syntax is incorrect."], can_be_deaf=True, can_be_blind=True)
        ]),
    Status.target_too_far_away : ViewMsgManager([
        UnformattedMsg(["Sorry, your target is too far away."], can_be_deaf=True,
        can_be_blind=True)
        ]),
    Status.impeding_affliction : ViewMsgManager([
        UnformattedMsg([
        "You can't do that while you are afflicted with: {afflictions}.",
        "Ack! While you still have {afflictions} you can't do that."],
        can_be_deaf=True, can_be_blind=True)
        ]),
    Status.attack_missed : ViewMsgManager([
        UnformattedMsg(["Doh! you missed!", "You swing and miss!"],
        can_be_deaf=True, can_be_blind=True)
        ]),
    Status.tile_doesnt_exist : ViewMsgManager([
        UnformattedMsg([
        "You might not want to go there.  There doesn't appear to exist."],
        can_be_deaf=True, can_be_blind=True)
        ]),
    Status.item_not_in_inventory : ViewMsgManager([
        UnformattedMsg(["{Item_name} is not in your inventory."],
        can_be_deaf=True, can_be_blind=True)
        ]),
    Status.equipment_slot_not_free : ViewMsgManager([
        UnformattedMsg(["That equipment slot is currently occupied.",
        "That equipment slot is not free."], can_be_deaf=True, can_be_blind=True)
        ]),
    Status.getting_nothing : ViewMsgManager([
        UnformattedMsg([
        "You should specify something to get before trying to get 'it'."],
        can_be_deaf=True, can_be_blind=True)
        ]),
    }


view_msg_managers = {
    MsgType.action_say : action_say_msg_manager,
    MsgType.action_say_to : action_say_to_msg_manager,
    MsgType.action_hit : action_hit_msg_manager,
    MsgType.action_move : action_move_msg_manager,
    MsgType.action_look_here : action_look_here_msg_manager,
    MsgType.action_get : action_get_msg_manager,
    MsgType.action_wear : action_wear_msg_manager,
    MsgType.action_wield : action_wield_msg_manager,
}


def format_msg(msg_info):
    msg_type = msg_info.get("msg_type")
    msgs = handle_msgs[msg_type](msg_info)
    try:
        formatted_msgs = []
        for entity, msg in msgs:
            new_msg = msg[0].upper() + msg[1:]
            formatted_msgs.append((entity, new_msg))
    except TypeError:
        #it must be a Status flag... just return msgs
        return msgs
    return formatted_msgs
