
from model.entity.basic_entity import Entity

class DeathInfo():

    def __init__(self, dead_guy):
        self.dead_guy = dead_guy.name
        self.body = Body(dead_guy)
        self.loot = set()
        self.xp_per_attacker = 0
        self.attackers = set()


class Body(Entity):

    def __init__(self, orig_guy):
        self.name = orig_guy.name
        self.permanent = orig_guy.permanent
        self.set_descriptions()
        self.loot = set()

    def set_descriptions(self):
        if self.permanent:
            self.short_desc = "{}'s body".format(self.name)
            self.long_desc = "Here lies {}'s body.  It's pretty gruesome.  You shouldn't look at it any more.".format(self.name)

    def __repr__(self):
        perm = "not " if not self.permanent else ""
        return "<dead_body: {} {}permanent>".format(self.name, perm)


def determine_who_gets_xp(entity):
    # This is used to determine who get's xp from a kill
    # The main idea is to start look at the dead_guy and who were
    #   his/her aggressors.  From the list of aggressors,
    #   look at who helped them.
    # Returns a list of people who should get xp

    attackers = set()

    # determine who recently attacked the entity
    # for each attacker:
    #   attackers.add(attacker)
    #   determine people who helped the attackers

    return attackers

