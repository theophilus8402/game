#!/usr/bin/python3

from model.msg import ActionMsgs
from .entity.player import handle_initial_player_connection
from .entity.blob import handle_blob_input


def world_get_input(world, readable):
    for s in readable:
        if s == world.server_socket:
            client, address = s.accept()
            print("Receiving a connection from {}...".format(address))
            # give the new connection a "home" in an entity
            handle_initial_player_connection(world, client)

        else:
            entity = world.socket_entity_map[s]
            data = entity.comms.recv()
            if data:
                command = data.split()[0]
                new_msg = ActionMsgs(cmd_word=command, msg=data, src_entity=entity)
                if entity.blob_state:
                    handle_blob_input(world, new_msg)
                elif command in entity.known_cmds:
                    world.immediate_action_msgs.put(new_msg)
                else:
                    entity.comms.send("Huh? What is {}".format(command))

