#!/usr/bin/python3

from view.msgs.basic import format_msg, MsgType

def send_error_msg(msg_info, error):
    msg_info["msg_type"] = MsgType.error
    msg_info["error_code"] = error
    msg_info["entities"] = [msg_info["actor"]]
    format_and_send_msg(msg_info)


def format_and_send_msg(msg_info):
    formatted_msgs = format_msg(msg_info)
    if formatted_msgs:
        for entity, msg in formatted_msgs:
            entity.comms.send(msg)

