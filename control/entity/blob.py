#!/usr/bin/python3

from control.entity.send_msg import format_and_send_msg
from model.entity.living.blob import States
from model.world import world_add_entity
from view.msgs.basic import format_msg, MsgType


def handle_blob_input(world, msg):
    entity = msg.src_entity
    blob_state = entity.blob_state
    msg_info = {
        "msg_type"  : MsgType.system, 
        "actor"     : entity,
        }
    if blob_state.state == States.expect_login_name:
        # get the name out of the msg
        temp_name = msg.msg.lower()
        # see if the name is legit
        # ask for a password
        if temp_name in world.living_ents.keys():
            str_msg = "States.expect_login_name. Found you: {}!".format(temp_name)
            entity.name = temp_name
            blob_state.state = States.expect_password
        else:
            str_msg = "States.expect_login_name. Here's the name: {}".format(temp_name)
        msg_info["msg"] = str_msg
        format_and_send_msg(msg_info)


    elif blob_state.state == States.expect_password:
        # get the password out of the msg
        passwd = msg.msg
        # see if the password is legit
        if passwd == entity.name:
            str_msg = "States.expect_password: Your password is correct!"
        else:
            str_msg = "States.expect_password: Not a good password!"
        msg_info["msg"] = str_msg
        format_and_send_msg(msg_info)
        # get the legit entity
        actual_entity = world.find_entity(entity.name)
        # shove the socket comms into that entity!
        actual_entity.comms = entity.comms
        world_add_entity(world, actual_entity)

