#!/usr/bin/python3.4

import enum

@enum.unique
class Status(enum.Enum):
    all_good = 0
    no_room_in_tile = 1
    entity_not_in_tile = 2
    killed_target = 3
