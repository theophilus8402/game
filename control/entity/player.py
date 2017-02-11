#!/usr/bin/python3

from control.comm import Socket_IO
from model.entity.living.blob import BlobState, States
from model.world import world_add_entity
from play import make_tim


class LogonEntity():
    def __init__(self):
        self.blob_state = BlobState(States.expect_login_name)
        self.comms = None


def handle_initial_player_connection(world, client_socket):
    temp_entity = LogonEntity()
    #temp_entity = make_tim()
    # create a new comms object with the client socket
    temp_entity.comms = Socket_IO(client_socket)
    # add the entity to the world
    # TODO: might not want to add the entity like this because then entity
    #   will be actually added to a tile in the world...
    input_handle = temp_entity.comms.get_input_handle()
    world.socket_entity_map[input_handle] = temp_entity
    #world_add_entity(world, temp_entity)
    # do I need to add him to a tile? I kinda want to say no
    # add the comms to the world
