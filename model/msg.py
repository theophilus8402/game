from datetime import datetime

class ActionMsgs():

    def __init__(self, cmd_word=None, msg=None, src_entity=None,
        time_submitted=datetime.now(), time_due=None):
        self.cmd_word = cmd_word
        self.msg = msg
        self.src_entity = src_entity
        self.time_submitted = time_submitted
        self.time_due = time_due

    def __str__(self):
        return "{}: {} - \"{}\" at {}".format(self.src_entity.name, 
            self.cmd_word, self.msg, self.time_submitted)
