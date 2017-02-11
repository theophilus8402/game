#!/usr/bin/python3

from model.util import RollType

from collections import defaultdict

class Human():

    def __init__(self):
        self.attack_possibilities = {
            RollType.critical_miss : 5,
            RollType.miss : 20,
            RollType.hit : 30,
            RollType.critical_hit : 5,
        }
        self.defence_possibilities = {
            RollType.dodge : 10,
            RollType.block : 0,
        }
