#!/usr/bin/python3.4

import enum
from collections import namedtuple

@enum.unique
class Status(enum.Enum):
    all_good = 0
    no_room_in_tile = 1
    entity_not_in_tile = 2
    killed_target = 3
    attack_missed = 4
    incorrect_syntax = 5
    target_doesnt_exist = 6
    target_too_far_away = 7
    tile_doesnt_exist = 8
    affliction_impeding = 9


class Coord(namedtuple("Coord", "x y")):

    def __sub__(self, other_coord):
        return Coord(other_coord.x - self.x, other_coord.y - self.y)

    def __add__(self, other_coord):
        return Coord(self.x + other_coord.x, self.y + other_coord.y)

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)


dir_coord_changes = {
    "n" : Coord(0, 1),
    "ne" : Coord(1, 1),
    "e" : Coord(1, 0),
    "se" : Coord(1, -1),
    "s" : Coord(0, -1),
    "sw" : Coord(-1, -1),
    "w" : Coord(-1, 0),
    "nw" : Coord(-1, 1)
}

