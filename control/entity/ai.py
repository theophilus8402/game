from datetime import datetime, timedelta
import random

def simple_get_next_cmd(self):
    """
    Needs:
        self.run_cmds
    """
    return random.choice(self.run_cmds)

def simple_set_next_run_time(self):
    """
    Needs:
        self.cmd_interval
    """
    rand_seconds = random.uniform(*self.cmd_interval)
    delta = timedelta(seconds=rand_seconds)
    self.next_run_time = datetime.now() + delta

def simple_run(self):
    """
    Needs:
        self.next_run_time
        self.get_next_cmd()
        self.comms.send_msg()   # these are msgs AI wants to send to game
        self.cmd_interval as a tuple
    """

    # get any input from the server
    comms = self.entity.comms
    msg = comms.read_from_server()
    while msg:
        msg = comms.read_from_server()

    # if it's time, get the next cmd to run
    if datetime.now() >= self.next_run_time:
        cmd = self.get_next_cmd()
        self.entity.comms.send_msg_to_server(cmd)

        self.set_next_run_time()


class Simple_AI(object):

    def __init__(self, entity):
        self.cmd_interval = (2, 5)
        self.set_next_run_time()
        self.run_cmds = []
        self.entity = entity

    set_next_run_time = simple_set_next_run_time
    get_next_cmd = simple_get_next_cmd
    run = simple_run

