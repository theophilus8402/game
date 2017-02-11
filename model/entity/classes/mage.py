#!/usr/bin/python3

from model.util import RollType

from collections import defaultdict

class Mage():

    def __init__(self):
        self.attack_possibilities = {
            RollType.critical_miss : 5,
            RollType.miss : 5,
            RollType.hit : 5,
            RollType.critical_hit : 0,
        }
        self.defence_possibilities = {
            RollType.dodge : 0,
            RollType.block : 0,
        }
