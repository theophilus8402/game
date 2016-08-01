#!/usr/bin/python3.4

import enum
from collections import namedtuple, defaultdict

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
    impeding_affliction = 9
    saying_nothing = 10
    cant_do_this_round = 11
    attack_hit = 12
    getting_nothing = 13
    item_too_big = 14
    item_too_heavy = 15


class Coord(namedtuple("Coord", "x y")):

    def __sub__(self, other_coord):
        return Coord(other_coord.x - self.x, other_coord.y - self.y)

    def __add__(self, other_coord):
        return Coord(self.x + other_coord.x, self.y + other_coord.y)

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)


dir_coord_changes = {
    "n" : Coord(0, 1),
    "north" : Coord(0, 1),
    "ne" : Coord(1, 1),
    "northeast" : Coord(1, 1),
    "e" : Coord(1, 0),
    "east" : Coord(1, 0),
    "se" : Coord(1, -1),
    "southeast" : Coord(1, -1),
    "s" : Coord(0, -1),
    "south" : Coord(0, -1),
    "sw" : Coord(-1, -1),
    "southwest" : Coord(-1, -1),
    "w" : Coord(-1, 0),
    "west" : Coord(-1, 0),
    "nw" : Coord(-1, 1),
    "northwest" : Coord(-1, 1),
}

dir_words = defaultdict(lambda: None)
dir_words["n"] = "north"
dir_words["north"] = "north"
dir_words["ne"] = "northeast"
dir_words["northeast"] = "northeast"
dir_words["e"] = "east"
dir_words["east"] = "east"
dir_words["se"] = "southeast"
dir_words["southeast"] = "southeast"
dir_words["s"] = "south"
dir_words["south"] = "south"
dir_words["sw"] = "southwest"
dir_words["southwest"] = "southwest"
dir_words["w"] = "west"
dir_words["west"] = "west"
dir_words["nw"] = "northwest"
dir_words["northwest"] = "northwest"

def get_dir_word(direction):
    return dir_words[direction]
