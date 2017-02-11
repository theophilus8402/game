#!/usr/bin/python3

import os
from select import select
from socket import socket, AF_INET, SOCK_STREAM
import sys
import time
from queue import Queue
from io import StringIO


class Communication(object):

    def send(self, msg):
        pass

    def recv(self):
        pass


class Std_IO(Communication):

    def __init__(self):
        """Sets the input_handle and output_handle to sys.stdin and sys.stdout."""
        self.input_handle = sys.stdin
        self.output_handle = sys.stdout

    def send(self, msg):
        """Sends a msg from the server to the entity's output_handle."""
        print(msg, file=self.output_handle)

    def recv(self):
        """Recieves a msg sent from the entity to the server."""
        data = self.input_handle.readline()
        return data.strip()

    def get_input_handle(self):
        return self.input_handle


#TODO: maybe have a way to read in a script file and run that to re-test sequences
class AI_IO(Communication):

    def __init__(self, ai_name="AI", from_server_file=None):
        """Initializes all the pipes/handles."""
        self.name = ai_name
        self.output_handle = sys.stdout     # not actual AI's output
        server_read_fd, client_write_fd = os.pipe()     # client -> server comms
        client_read_fd, server_write_fd = os.pipe()     # server -> client comms
        self.server_read_handle = os.fdopen(server_read_fd, "rt")
        self.client_read_handle = os.fdopen(client_read_fd, "rt")
        self.server_write_handle = os.fdopen(server_write_fd, "wt")
        self.client_write_handle = os.fdopen(client_write_fd, "wt")
        self.read_from_server_file = from_server_file

    def __del__(self):
        """Cleans up all the open handles to the pipes... Hopefully..."""
        self.server_read_handle.close()
        self.client_read_handle.close()
        self.server_write_handle.close()
        self.client_write_handle.close()

    def send(self, msg):
        """Sends a msg from the server to the AI via a pipe."""
        #print("{} recv'd: {}".format(self.name, msg), file=self.output_handle)
        #self.server_write_handle.write("{}\n".format(msg))
        #TODO gotta go back to the line above, but I don't know how to fix multi-lines
        self.server_write_handle.write("{}\n".format(msg.replace("\n", "")))
        self.server_write_handle.flush()

    def read_from_server(self):
        """Reads a msg from the server to the AI via a pipe. Returns the msg."""
        readable, writeable, executable = select([self.client_read_handle],[],[],.08)
        msg = None
        if readable:
            msg = self.client_read_handle.readline()
            if self.read_from_server_file:
                with open(self.read_from_server_file, "at") as f:
                    f.write(msg)
        return msg

    def send_msg_to_server(self, msg):
        """Sends a msg from the AI to the server."""
        self.client_write_handle.write("{}\n".format(msg))
        self.client_write_handle.flush()
        #print("Server: {} .send_msg_to_server: {}".format(self.name, msg),
        #    file=self.output_handle)

    def recv(self):
        """Reads a msg from the AI to the server. Returns the msg."""
        data = self.server_read_handle.readline()
        #print("Server: {} .recv: {}".format(self.name, data), file=self.output_handle)
        return data

    def get_input_handle(self):
        return self.server_read_handle

"""
#TODO:
class Server_IO(Communication):

def __init__(self, s=None, world=None):     # maybe I can give it a ref here

recv() will be used to handle new incomming connections.  It will not return
data... or will it?  How will I attach new sockets to the world? I bet I
need to make the server have some "commands" to add new sockets/players.
"""


class Socket_IO(Communication):

    def __init__(self, s=None):
        if s:
            self.socket = s

    def send(self, msg):
        if isinstance(msg, str):
            msg += "\n"
            msg = msg.encode("utf-8")
        self.socket.send(msg)

    def recv(self):
        data = self.socket.recv(1024).decode("utf-8").strip()
        return data

    def get_input_handle(self):
        return self.socket

def start_server(world, ip, port):
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(10)
    world.server_socket = server_socket
    world.socket_entity_map[server_socket] = None


if __name__ == "__main__":

    st = File_IO()
    st.send("Howdy!")
    data = st.recv()
    if data:
        print(data)

    #m1 = Msg(data, "bob")
    #print("msg: {}... time: {} entity: {}".format(m1.msg, m1.time_recvd, m1.entity))
