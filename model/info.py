#!/usr/bin/python3.4

import enum

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


dir_coord_changes = {
    "n" : (0, 1),
    "ne" : (1, 1),
    "e" : (1, 0),
    "se" : (1, -1),
    "s" : (0, -1),
    "sw" : (-1, -1),
    "w" : (-1, 0),
    "nw" : (-1, 1)
}

