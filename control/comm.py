#!/usr/bin/python3

import sys
import time

class Msg(object):

    def __init__(self, msg=None, entity=None):
        self.msg = msg
        self.time_recvd = time.time()   # time in float seconds from epoc
        self.entity = entity


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

    m1 = Msg(data, "bob")
    print("msg: {}... time: {} entity: {}".format(m1.msg, m1.time_recvd, m1.entity))
