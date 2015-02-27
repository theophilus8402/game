#!/usr/bin/python3.4

import ui.text

make_tile_handle = False
make_tile_handle_symbol = False
make_tile_handle_ground = False

def make_tile(bob, msg, direction):
    if !(make_tile_handle_symbol or make_tile_handle_ground):
        ui.text.add_msg(bob, "You want to add a tile in this direction: {}?"
            .format(direction))
        make_tile_handle_symbol = True
        make_tile_handle = True
        ui.text.add_msg(bob, "What symbol? ")

    # TODO: make sure the tiles don't exist


def make_tile_handle(bob, msg):
    # got through a default set of questions... hrm... how do I do this?
        # solving this ties in with handling quests
    if make_tile_handle_symbol:
        # TODO: check for appropriate symbol

        symbol = msg
        make_tile_handle_symbol = False
