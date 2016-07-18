
import enum
import random
from collections import defaultdict

from view.info import ViewStatus
from model.entity.entity import Living
from model.entity.status_effects import Body, check_health
from model.info import Status

@enum.unique
class MsgType(enum.Enum):
    system = 0
    action_say = 1
    error = 2
    action_hit = 3
    action_move = 4
    action_say_to = 5

error_code_msgs = {
    Status.saying_nothing : ["Erm... you didn't actually say anything.",
        "Uh... you didn't say any words.  wanna try again?"],
    Status.target_doesnt_exist : [
        "Either that entity doesn't exist or isn't close by.",
        "To whom are you referring?"],
    Status.cant_do_this_round : ["You can't do that this round.",
        "Whoa there, slow down.  You need to wait until next turn."],
    Status.incorrect_syntax : ["Syntax is incorrect."],
    Status.target_too_far_away : ["Sorry, your target is too far away."],
    Status.impeding_affliction : [
        "You can't do that while you are afflicted with: {afflictions}.",
        "Ack! While you still have {afflictions} you can't do that."],
    Status.attack_missed : ["Doh! you missed!", "You swing and miss!"],
    Status.tile_doesnt_exist : [
        "You might not want to go there.  There doesn't appear to exist."],
    }



def format_error_msg(msg_info):
    # Must return a list of (entity, msg) tuples
    code = msg_info["error_code"]
    entity = msg_info["actor"]
    msg = random.choice(error_code_msgs[code])
    formatted_msg = msg.format(**msg_info)
    return [(entity, formatted_msg)]


def format_system_msg(msg_info):
    # Must return a list of (entity, msg) tuples
    entity = msg_info["actor"]
    msg = msg_info["msg"].format(**msg_info)
    return [(entity, msg)]


def make_format_string_dict(info, entity):
    md = {}

    actor = None
    if "actor" in info:
        actor = info["actor"]
        md["actor"] = "you" if entity == actor else actor.name
        md["Actor"] = "You" if entity == actor else actor.name
        md["action_move"] = "move" if entity == actor else "moves"
        md["action_skip"] = "skip" if entity == actor else "skips"
        md["action_say"] = "say" if entity == actor else "says"
        md["action_hit"] = "hit" if entity == actor else "hits"
        if entity == actor:
            md["actor_poss"] = "your"
        else:
            md["actor_poss"] = "his" if actor.male else "her"

    if "recip" in info:
        recipient = info["recip"]
        if actor and (entity == recipient) and (entity == actor):
            md["recip"] = "yourself"
            md["Recip"] = "Yourself"
            md["recip_poss"] = "your"
        elif entity == recipient:
            md["recip"] = "you"
            md["Recip"] = "You"
            md["recip_poss"] = "your"
        elif actor and actor == recipient:
            md["recip"] = "himself" if recipient.male else "herself"
            md["Recip"] = "Himself" if recipient.male else "Herself"
            md["recip_poss"] = "his" if recipient.male else "her"
        else:
            md["recip"] = recipient.name
            md["Recip"] = recipient.name
            md["recip_poss"] = "his" if recipient.male else "her"

    for key, value in info.items():
        if key not in md:
            md[key] = value

    return md


def format_action_msg(msg_info):
    msg_type = msg_info.get("msg_type")
    entities = msg_info.get("entities")
    actor = msg_info.get("actor")
    recipient = msg_info.get("recipients")
    if recipient:
        recipient = recipient[0]   #TODO: allow for multiple recipients
        msg_info["recip"] = recipient
    formatted_msgs = []
    for entity in entities:
        unformatted_msg = get_unformatted_msg(msg_type, entity, actor, recipient)
        if unformatted_msg:
            msg_strings = make_format_string_dict(msg_info, entity)
            formatted_msgs.append((entity, unformatted_msg.format(**msg_strings)))
    return formatted_msgs


handle_msgs = defaultdict(lambda: format_action_msg)
handle_msgs[MsgType.system] = format_system_msg
handle_msgs[MsgType.error] = format_error_msg


@enum.unique
class EntStatus(enum.Enum):
    healthy = 0
    blind = 1
    deaf = 2
    blind_and_deaf = 3
    blind_recip = 4
    deaf_recip = 5
    blind_and_deaf_recip = 6


unformatted_msgs = {
    MsgType.action_say : {
        EntStatus.healthy : ["{Actor} {action_say}, '{words}'"],
        EntStatus.deaf : ["You see {actor} moving {actor_poss} lips but can't hear anything."],
        EntStatus.blind : ["You hear someone say, '{words}'"],
        EntStatus.blind_and_deaf : None,
        },
    MsgType.action_say_to : {
        EntStatus.healthy : ["{Actor} {action_say} to {recip}, '{words}'"],
        EntStatus.deaf : ["You see {actor} moving {actor_poss} lips but can't hear anything."],
        EntStatus.blind : ["You hear someone say, '{words}'"],
        EntStatus.blind_and_deaf : None,
        EntStatus.deaf_recip : ["You see {actor} moving {actor_poss} lips but can't hear anything."],
        EntStatus.blind_recip : ["You hear someone say, '{words}'"],
        EntStatus.blind_and_deaf_recip : None,
        },
    MsgType.action_hit : {
        EntStatus.healthy : ["{Actor} maliciously {action_hit} {recip}!"],
        EntStatus.deaf : ["{Actor} maliciously {action_hit} {recip}!"],
        EntStatus.blind : ["You hear some fighting going on nearby."],
        EntStatus.blind_and_deaf : None,
        EntStatus.deaf_recip : ["{Actor} maliciously {action_hit} {recip}!"],
        EntStatus.blind_recip : ["Someone hit you!"],
        EntStatus.blind_and_deaf_recip : ["Someone hit you!"],
        },
    MsgType.action_move : {
        EntStatus.healthy : [ "{Actor} {action_move} to the {dir}.",
                              "{Actor} {action_skip} to the {dir}."],
        EntStatus.blind :   [ "You hear someone nearby move."],
        EntStatus.deaf :    [ "{Actor} {action_move} to the {dir}.",
                              "{Actor} {action_skip} to the {dir}."],
        },
    }


def get_unformatted_msg(msg_type, entity, actor=None, recip=None):
    if entity != actor:
        # the actor should know if he said the words regardless of being deaf
        deaf = check_health(entity, {Body.ears})
        blind = check_health(entity, {Body.eyes})
        if deaf and blind:
            if entity == recip:
                choices = unformatted_msgs[msg_type][EntStatus.blind_and_deaf_recip]
            else:
                choices = unformatted_msgs[msg_type][EntStatus.blind_and_deaf]
        elif blind:
            if entity == recip:
                choices = unformatted_msgs[msg_type][EntStatus.blind_recip]
            else:
                choices = unformatted_msgs[msg_type][EntStatus.blind]
        elif deaf:
            if entity == recip:
                choices = unformatted_msgs[msg_type][EntStatus.deaf_recip]
            else:
                choices = unformatted_msgs[msg_type][EntStatus.deaf]
        else:
            choices = unformatted_msgs[msg_type][EntStatus.healthy]
    else:
        choices = unformatted_msgs[msg_type][EntStatus.healthy]
    if isinstance(choices, list) and len(choices) > 0:
        unformatted_msg = random.choice(choices)
    else:
        unformatted_msg = None
    return unformatted_msg


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
