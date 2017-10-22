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
    eqslot_not_free = 16
    improper_eq_slot = 17
    item_not_in_inventory = 18
    item_not_in_equipment = 19
    invalid_eqslot = 20
    eqslot_empty = 21

