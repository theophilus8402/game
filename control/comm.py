#!/usr/bin/python3

import os
import sys
import time
from queue import Queue
from io import StringIO

"""
class Msg(object):

    def __init__(self, msg=None, entity=None):
        self.msg = msg
        self.time_recvd = time.time()   # time in float seconds from epoc
        self.entity = entity
"""


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


"""
#TODO:
class Scripted_IO(Communication):

If random=False, this IO class will read in a file and execute/send those
commands in order but at random times.  This will allow for "live" testing
or a series of tests to be conducted.

If random=True, this class will read in a file that dictates all commands
that I want tested (even random junk).  It will execute/send those
commands at random intervals.  This class will keep on going until given
a key word by the system to exit.
"""
class AI_IO(Communication):

    def __init__(self, ai_name="AI"):
        self.outbox = Queue()     # what the AI sends out
        self.inbox = Queue()      # what the AI receives
        self.name = ai_name
        self.output_handle = sys.stdout     # not actual AI's output
        # Aha!  I need to use os.pipe... this will give me similar functionality to sockets and let me use select on em...
        server_read_fd, client_write_fd = os.pipe()     # client -> server comms
        client_read_fd, server_write_fd = os.pipe()     # server -> client comms
        self.server_read_handle = os.fdopen(server_read_fd, "rt")
        self.client_read_handle = os.fdopen(client_read_fd, "rt")
        self.server_write_handle = os.fdopen(server_write_fd, "wt")
        self.client_write_handle = os.fdopen(client_write_fd, "wt")
        

    def send(self, msg):    # data being sent TO the AI
        print("Server: {} got: {}".format(self.name, msg), file=self.output_handle)
        #self.inbox.put(msg)
        self.server_write_handle.write("{}\n".format(msg))
        self.server_write_handle.flush()

    def send_msg_to_server(self, msg):    
        #print("Adding to outbox: {}".format(msg))
        #self.outbox.put(msg)
        self.client_write_handle.write("{}\n".format(msg))
        self.client_write_handle.flush()
        print("Server: {} .send_msg_to_server: {}".format(self.name, msg))

    def recv(self):         # data the AI has sent to the game
        #try:
        #    data = self.outbox.get_nowait().strip()
        #except:
        #    data = None
        data = self.server_read_handle.readline()
        print("Server: {} .recv: {}".format(self.name, data))
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
