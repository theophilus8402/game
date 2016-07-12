
import enum
import random

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
        "You can't do that while you are afflicted with: {affliction}.",
        "Ack! While you still have {affliction} you can't do that."],
    Status.attack_missed : ["Doh! you missed!", "You swing and miss!"],
    Status.tile_doesnt_exist : [
        "You might not want to go there.  There doesn't appear to exist."],
    }


@enum.unique
class SuccessType(enum.Enum):
    success = 0
    blind = 1
    deaf = 2
    blind_and_deaf = 3

successful_msgs = {
    MsgType.action_move : {
        SuccessType.success : [ "{actor} {move} to the {dir}.",
                                "{actor} {skips} to the {dir}."],
        SuccessType.blind :   [ "You hear someone nearby move."],
        SuccessType.deaf :    [ "{actor} {move} to the {dir}.",
                                "{actor} {skips} to the {dir}."],
        },
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


def format_action_move_msg(msg_info):
    actor = msg_info.get("actor")
    recipients = msg_info.get("recipients")
    entities = msg_info.get("entities")



def format_action_hit_msg(msg_info):
    actor = msg_info.get("actor")
    recipients = msg_info.get("recipients")
    entities = msg_info.get("entities")

    normal_msg = "{actor} maliciously hit {recip}!"

    if len(recipients) != 1:
        return ViewStatus.too_many_recipients

    recipient = recipients[0]

    personalized_msg_info = {}
    msgs_to_send = []
    entities = (ent for ent in entities if isinstance(ent, Living))
    for entity in entities:
        if entity == actor:
            personalized_msg_info["actor"] = "You"
        else:
            personalized_msg_info["actor"] = actor.name

        if entity == recipient:
            personalized_msg_info["recip"] = "you"
        else:
            personalized_msg_info["recip"] = recipient.name

        msgs_to_send.append((entity, normal_msg.format(**personalized_msg_info)))

    return msgs_to_send


def format_action_say_msg(msg_info):
    # every action_say msg_info should contain at least the following:
    say_to = msg_info.get("say_to")
    actor = msg_info.get("actor")
    recipients = msg_info.get("recipients")
    words = msg_info.get("words")
    entities = msg_info.get("entities")

    if len(recipients) > 1:
        #print("ERROR: there are too many recipients listed in {}.".format(msg_info))
        return ViewStatus.too_many_recipients

    fail_sound_msg = "You see {actor} moving {his} lips but can't hear anything."
    fail_sight_msg = "You hear someone say, '{msg}'"

    if say_to and recipients:
        normal_msg = "{actor} {say} to {recip}, '{msg}'"
        recipient = recipients[0]
    elif say_to and not recipients:
        #print("ERROR: missing recipient info in {msg}.".format(msg=msg_info))
        return ViewStatus.missing_msg_info
    else:
        normal_msg = "{actor} {say}, '{msg}'"

    msgs_to_send = []
    personalized_msg_info = {}
    personalized_msg_info["his"] = "his" if actor.male else "her"
    entities = (ent for ent in entities if isinstance(ent, Living))
    for entity in entities:
        if entity == actor:
            personalized_msg_info["actor"] = "You"
            personalized_msg_info["say"] = "say"
        else:
            personalized_msg_info["actor"] = actor.name
            personalized_msg_info["say"] = "says"

        if say_to:
            if (entity == recipient) and (entity == actor):
                personalized_msg_info["recip"] = "yourself"
            elif entity == recipient:
                personalized_msg_info["recip"] = "you"
            elif actor == recipient:
                personalized_msg_info["recip"] = "himself" if actor.male else "herself"
            else:
                personalized_msg_info["recip"] = recipient.name
        personalized_msg_info["msg"] = words

        # determine if their blind or deaf and send the appropriate msg
        unformatted_msg = normal_msg
        if entity != actor:
            # the actor should know if he said the words regardless of being deaf
            deaf = check_health(entity, {Body.ears})
            blind = check_health(entity, {Body.eyes})
            if deaf and blind:
                # no msg should be sent to the entity
                continue
            elif blind:
                unformatted_msg = fail_sight_msg
            elif deaf:
                unformatted_msg = fail_sound_msg
        msg = unformatted_msg.format(**personalized_msg_info)
        msgs_to_send.append((entity, msg))
    return msgs_to_send


handle_msgs = {
    MsgType.system : format_system_msg,
    MsgType.action_say : format_action_say_msg,
    MsgType.error : format_error_msg,
    MsgType.action_hit : format_action_hit_msg,
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
