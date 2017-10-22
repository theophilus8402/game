#!/usr/bin/python3

from collections import defaultdict,namedtuple


class Coord(namedtuple("Coord", "x y")):

    def __sub__(self, other_coord):
        return Coord(other_coord.x - self.x, other_coord.y - self.y)

    def __add__(self, other_coord):
        return Coord(self.x + other_coord.x, self.y + other_coord.y)

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)


direction_coords = {
    "n": Coord(0, 1),
    "north": Coord(0, 1),
    "ne": Coord(1, 1),
    "northeast": Coord(1, 1),
    "e": Coord(1, 0),
    "east": Coord(1, 0),
    "se": Coord(1, -1),
    "southeast": Coord(1, -1),
    "s": Coord(0, -1),
    "south": Coord(0, -1),
    "sw": Coord(-1, -1),
    "southwest": Coord(-1, -1),
    "w": Coord(-1, 0),
    "west": Coord(-1, 0),
    "nw": Coord(-1, 1),
    "northwest": Coord(-1, 1),
}


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

