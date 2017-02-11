#!/usr/bin/python3

import enum

@enum.unique
class States(enum.Enum):
    expect_login_name = 0
    expect_password = 1
    expect_response_to_quest = 2


class BlobState():

    def __init__(self, state):
        self.state = state
        self.info = {}


