#!/usr/bin/python3.4

import socket
import select
import queue
import sys
import model.tile
import control.uinput

# http://pymotw.com/2/select/


# sends all messages in bob's msg_queue
def actually_send_msgs(world, bob):
    s = bob.sock
    while True:
        try:
            next_msg = bob.msg_queue.get_nowait()
        except queue.Empty:
            #print("Output queue for {} is empty.".format(s.getpeername()))
            if s in world.outputs:
                world.outputs.remove(s)
            break
        else:
            print("Sending {}... to {}".format(next_msg, s.getpeername()))
            s.send(next_msg)
    return True


# msg should always be a string with no '\n'
def send_msg(world, bob, msg):
    bmsg = b''
    try:
        # make sure msg is a bytearray
        # will error if msg is already a bytearray
        bmsg = bytearray("{}\n".format(msg), "utf-8")
    except:
        bmsg = msg + b'\n'
    bob.msg_queue.put(bmsg)
    if bob.sock not in world.outputs:
        world.outputs.append(bob.sock)
    return True


# should get a world, socket, and a Entity object
# TODO: I don't check for multiple bob's
def add_connection(world, sock, bob):
    bob.sock = sock
    world.sock_peeps[sock] = bob
    return True


def remove_connection(world, sock):
    del world.sock_peeps[sock]
    if sock in world.outputs:
        world.outputs.remove(sock)
    sock.close()
    return True


def find_bob(world, name):
    ret_bob = None
    for bob in world.entities:
        if bob.name.lower() == name.lower():
            ret_bob = bob
            break
    return ret_bob


def transfer_bobs(world, temp_entity, entity):
    # temp_entity is the entity that has the sock
    entity.sock = temp_entity.sock

    # change world.sock_peeps from temp_entity to entity
    world.sock_peeps[temp_entity.sock] = entity

    return entity


def login(world, bob, msg=None):

    if (bob.state == "login") and (not msg):
        # send: who are you?
        if bob.name is None:
            send_msg(world, bob, "What is your name? ")
    elif bob.state == "login":
        # get: name
        if not bob.name:
            send_msg(world, bob, "Ah, so your name is {}?".format(msg))
            if msg in world.passwds.keys():
                # assign his name
                bob.name = msg
                # send: what's your password?
                send_msg(world, bob, "Please enter your password: ")
            else:
                send_msg(world, bob,
                    "Sorry! You don't exist! Gimme a new name: ")
        else:
            # get: passwd
            # check password
            if world.passwds[bob.name] == msg:
                send_msg(world, bob, "Hey! Your password is correct!")
                # return the actual bob entity
                entities_bob = find_bob(world, bob.name)
                if entities_bob:
                    bob = transfer_bobs(world, bob, entities_bob)
                    bob.special_state = False
                    bob.state = None
                else:
                    print("Eeep!  I couldn't find: {}".format(bob.name))
                    bob.name = None
                    login(world, bob)
            else:
                send_msg(world, bob, "Sorry! Wrong password!")
    # if we got here when bob.state was not login, do nothing
    return True


def server_loop(world):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    host = "127.0.0.1"
    port = 12345
    server.bind((host, port))

    server.listen(5)
    conn_count = 0

    server_guy = model.tile.Entity()
    server_guy.name = "server"
    server_guy.special_state = False    # server doesn't need to login
    server_guy.state = None
    add_connection(world, server, server_guy)


    timeout = .1
    continue_loop = True
    while continue_loop:
        readable, writable, exceptional = select.select(
            world.sock_peeps.keys(), world.outputs,
            world.sock_peeps.keys(), timeout)

        for s in readable:

            if s is server:
                # a readable server socket means it's ready to accept a conn
                connection, client_addr = s.accept()
                print("New connection from {}".format(client_addr))
                connection.setblocking(0)
                bob = model.tile.Entity()
                add_connection(world, connection, bob)
                login(world, bob)
            elif s is sys.stdin:
                # stdin input!
                data = s.readline().strip()
                if data:
                    print("Recieved from stdin: {}".format(data))
                    if data == "exit":
                        continue_loop = False
                        server.close()
            else:
                # someone sent me something!
                data = s.recv(1024)
                if data:
                    print("Recieved: {} from {}".format(data,
                        s.getpeername()))
                    bob = world.sock_peeps[s]
                    msg = data.decode("utf-8").strip()
                    send_msg(world, bob, msg)
                    if s not in world.outputs:
                        world.outputs.append(s)
                    # handle it
                    #handle_input(world, bob, msg)
                    control.uinput.handle_user_input(world, bob, msg)
                else:
                    # data is empty means the client closed the connection
                    print("Closing {}...".format(s.getpeername()))
                    remove_connection(world, s)

        for s in writable:
            actually_send_msgs(world, world.sock_peeps[s])

        for s in exceptional:
            print("Handling exceptional condition for {}".format(
                s.getpeername()))
            remove_connection(world, s)
    return True


if __name__ == "__main__":

    """
    import model.tile
    bob = model.tile.Entity()
    """

    world = World()
    world.passwds["bob"] = "bob123"
    world.passwds["tom"] = "tom123"
    world.passwds["cat"] = "cat123"
    world.passwds["sam"] = "sam123"

    server_loop(world)
