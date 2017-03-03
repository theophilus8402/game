#!/usr/bin/python3

from model.util import RollType

from collections import defaultdict

class Mage():

    def __init__(self):
        self.possibilities = {
            # attack stuff
            RollType.critical_miss : 5,
            RollType.miss : 5,
            RollType.hit : 5,
            RollType.critical_hit : 0,

            # defences
            RollType.dodge : 0,
            RollType.block : 0,
        }
