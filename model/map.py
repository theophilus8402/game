#!/usr/bin/python3

from collections import defaultdict

from model.world import Coord

class Map():

    def __init__(self, top_left_coords, bottom_right_coords, base_symbol):
        self.min_x, self.max_y = top_left_coords
        self.max_x, self.min_y = bottom_right_coords
        self.base_symbol = base_symbol

        # TODO: I bet I could do something creative here to handle passing a
        #   " " instead of the default symbol
        self._map = defaultdict(lambda: defaultdict(lambda: self.base_symbol))

    def add_symbol(self, coords, symbol):
        x, y = coords
        self._map[x][y] = symbol

    def remove_symbol(self, coords):
        x, y = coords
        del(self._map[x][y])

    def get_map(self, center_coords, radius):
        center_x, center_y = center_coords
        temp_map = []
        for y in range(center_y+radius, center_y-radius-1, -1):
            row = [self._map[x][y] for x in
                    range(center_x-radius, center_x+radius+1)]
            temp_map.append("".join(row))
        return temp_map

