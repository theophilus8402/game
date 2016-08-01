#!/usr/bin/python3

from time import time


class RoundInfo():

    def __init__(self):
        self.time_started = time()
        self.feet_moved = 0
        self.num_attacks = 0
        #self.last_time_moved = None
        #self.last_time_left_attacked = None
        #self.last_time_right_attacked = None
        self.interacted_obj = False
        self.other_action = False


def check_new_round(entity):
    round_length = 4
    current_time = time()
    round_info = entity.round_info
    if (current_time >= (round_info.time_started + round_length)):
        round_info.time_started = current_time
        round_info.feet_moved = 0
        round_info.num_attacks = 0
        round_info.interacted_obj = False
        round_info.other_action = False


def round_info_can_interact_obj(entity):
    check_new_round(entity)
    return not entity.round_info.interacted_obj


def round_info_entity_interacted_w_obj(entity):
    entity.round_info.interacted_obj = True
