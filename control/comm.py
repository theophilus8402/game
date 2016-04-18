#!/usr/bin/python3

import os
from select import select
import sys
import time
from queue import Queue
from io import StringIO


class Communication(object):

    def send(self, msg):
        pass

    def recv(self):
        pass


class File_IO(Communication):

    def __init__(self, input_handle=None, output_handle=None):
        if input_handle:
            self.input_handle = input_handle

            if output_handle is None:
                self.output_handle = input_handle  # output is same as in
            else:
                self.output_handle = output_handle
        
        else:       # using stdin/stdout
            self.input_handle = sys.stdin

            if output_handle is None:
                self.output_handle = sys.stdout
            else:
                self.output_handle = output_handle

    def send(self, msg):
        print(msg, file=self.output_handle)

    def recv(self):
        data = self.input_handle.readline()
        return data.strip()


#TODO: maybe have a way to read in a script file and run that to re-test sequences
class AI_IO(Communication):

    def __init__(self, ai_name="AI", from_server_file=None):
        self.name = ai_name
        self.output_handle = sys.stdout     # not actual AI's output
        server_read_fd, client_write_fd = os.pipe()     # client -> server comms
        client_read_fd, server_write_fd = os.pipe()     # server -> client comms
        self.server_read_handle = os.fdopen(server_read_fd, "rt")
        self.client_read_handle = os.fdopen(client_read_fd, "rt")
        self.server_write_handle = os.fdopen(server_write_fd, "wt")
        self.client_write_handle = os.fdopen(client_write_fd, "wt")
        self.read_from_server_file = from_server_file
        

    def send(self, msg):    # send data TO the AI
        #print("{} recv'd: {}".format(self.name, msg), file=self.output_handle)
        self.server_write_handle.write("{}\n".format(msg))
        self.server_write_handle.flush()

    def read_from_server(self):     # read msgs that were sent to the AI
        readable, writeable, executable = select([self.client_read_handle],[],[],.08)
        msg = None
        if readable:
            msg = self.client_read_handle.readline()
            if self.read_from_server_file:
                with open(self.read_from_server_file, "at") as f:
                    f.write(msg)
        return msg

    def send_msg_to_server(self, msg):    
        self.client_write_handle.write("{}\n".format(msg))
        self.client_write_handle.flush()
        print("Server: {} .send_msg_to_server: {}".format(self.name, msg),
            file=self.output_handle)

    def recv(self):         # data the AI has sent to the game
        data = self.server_read_handle.readline()
        #print("Server: {} .recv: {}".format(self.name, data), file=self.output_handle)
        return data

"""
#TODO:
class Server_IO(Communication):

def __init__(self, s=None, world=None):     # maybe I can give it a ref here

recv() will be used to handle new incomming connections.  It will not return
data... or will it?  How will I attach new sockets to the world? I bet I
need to make the server have some "commands" to add new sockets/players.
"""


#TODO:
class Socket_IO(Communication):

    def __init__(self, s=None):
        if s:
            self.socket = s

    def send(self, msg):
        pass

    def recv(self):
        pass


if __name__ == "__main__":

    st = File_IO()
    st.send("Howdy!")
    data = st.recv()
    if data:
        print(data)

    #m1 = Msg(data, "bob")
    #print("msg: {}... time: {} entity: {}".format(m1.msg, m1.time_recvd, m1.entity))
