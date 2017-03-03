#!/usr/bin/python3

from model.util import RollType

from collections import defaultdict

class Human():

    def __init__(self):
        self.possibilities = {
            # attack stuff
            RollType.critical_miss : 5,
            RollType.miss : 20,
            RollType.hit : 30,
            RollType.critical_hit : 5,

            # defenses
            RollType.dodge : 10,
            RollType.block : 0,
        }
