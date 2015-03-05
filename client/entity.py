#!/usr/bin/python3.4

class Entity:

    def __init__(self):
        self.map_win = None
        self.text_win = None
        self.cmd_win = None
        self.disp_msgs = []   # temporary, recalculated when win resized
        self.msg_len = 3000
        self.disp_msg_start = 0
        self.text_scroll = True

