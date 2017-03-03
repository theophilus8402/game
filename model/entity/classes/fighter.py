#!/usr/bin/python3

from model.util import RollType

from collections import defaultdict

class Fighter():

    def __init__(self):
        self.possibilities = {
            # attack stuff
            RollType.critical_miss : 0,
            RollType.miss : 0,
            RollType.hit : 15,
            RollType.critical_hit : 5,

            # defences
            RollType.dodge : 5,
            RollType.block : 5,
        }
