
import select

from model.map import Coord,direction_coords

input_map = {}

def get_all_input(self, timeout=.1):

    readable, writable, exceptional = select.select(
        self.socket_entity_map, [], [], timeout)

    all_input = []

    for s in readable:
        if s == self.server_socket:
            client, address = s.accept()
            print("Receiving a connection from {}...".format(address))
            # give the new connection a "home" in an entity
            handle_initial_player_connection(self, client)

        else:
            entity = self.socket_entity_map[s]
            data = entity.comms.recv()
            if data:
                all_input.append((entity, data.strip()))
                """
                command = data.split()[0]
                new_msg = ActionMsgs(cmd_word=command, msg=data, src_entity=entity)
                if entity.blob_state:
                    handle_blob_input(world, new_msg)
                elif command in entity.known_cmds:
                    world.immediate_action_msgs.put(new_msg)
                else:
                    entity.comms.send("Huh? What is {}".format(command))
                """
    return all_input


def handle_input(self, entity, input_str):

    print("{} sent: '{}'".format(entity.name, input_str))
    pieces = input_str.split()
    action = input_map.get(pieces[0])
    if action:
        action(self, entity, input_str)
    else:
        print("That's not an action!")

def input_move(self, entity, input_str):

    # TODO: check to see if entity can actually walk
    # TODO: check to see if entity can move into that spot

    # determine the new coords
    new_coords = entity.coords + direction_coords[input_str]

    # move the entity
    self.move_entity(entity, new_coords)

    # TODO: deduct the movement from the entities available actions

# add all the movement actions to the input_map
for direction in direction_coords:
    input_map[direction] = input_move

def input_look(self, entity, input_str):

    # TODO: see if you can actually look

    # look
    self.action_look(entity)

# add all the look actions to the input_map
input_map["l"] = input_look
input_map["look"] = input_look

