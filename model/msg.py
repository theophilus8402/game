from datetime import datetime, timedelta


class Msgs():

    def __init__(self, target=None, time_delta=None, status=None,
        recurring=False):
        self.target = target
        self.time_submitted = datetime.now()
        self.time_delta = time_delta
        if time_delta:
            self.set_due()
        else:
            self.time_due = None
        self.status = status
        self.recurring=recurring

    def check(self):
        return datetime.now() >= self.time_due

    def execute(self):
        if self.status == "meditate":
            if "meditating" in self.target.status_msgs:
                self.target.send_msg("{} regains some more mp...".format(
                    self.target.name))
                self.target.change_mp(4)
            else:
                self.recurring=False # makes sure msg will get deleted
        else:
            #TODO: implement this
            self.target.send_msg("Removing {} from {}...".format(
                self.status, self.target.name))

        if self.recurring:
            self.set_due()
        return self.recurring

    def set_due(self):
        self.time_due = datetime.now() + self.time_delta

    def __str__(self):
        return "{}: {}".format(self.target.__str__(), self.execute.__str__())
