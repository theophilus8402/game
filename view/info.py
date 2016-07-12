#!/usr/bin/python3.4

import enum
from collections import namedtuple

@enum.unique
class ViewStatus(enum.Enum):
    all_good = 0
    too_many_recipients = 1
    missing_msg_info = 2
    not_enough_speed = 3
    used_all_attacks = 4
