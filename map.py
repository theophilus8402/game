#!/usr/bin/python3

from collections import defaultdict, namedtuple
from copy import deepcopy
import time
from timeit import timeit

"""
Now, I should test putting sensors down.
Two different methods:
    1) sensors keep track of distance for sight and hearing
    2) sensors just keep "as the crow flies" distance and then use A* to
        calculate the other distances
"""

Coord = namedtuple("Coord", ["x", "y"])
#Distances = namedtuple("Distances", ["physical", "hearing", "sight"])

class Coord(namedtuple("Coord", "x y")):
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    """

    def __add__(self, other_coord):
        return Coord(self.x + other_coord.x, self.y + other_coord.y)

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)


class Distances(object):
    def __init__(self, physical, hearing, sight):
        self.physical = physical
        self.hearing = hearing
        self.sight = sight

    def __add__(self, delta):
        return Distances(self.physical + delta.physical, self.hearing +
            delta.hearing, self.sight + delta.sight)


class Sense(object):
    def __init__(self, entity, pcoord, distances):
        self.entity = entity
        self.pcoord = pcoord
        self.distances = distances

    def __repr__(self):
        return "{} : {}/{}/{}".format(self.entity.name,
            self.distances.physical, self.distances.hearing,
            self.distances.sight)


def remove_sense_tile(sense, tile):
    try:
        tile.senses.remove(sense)
    except:
        print("Can't remove: {} from {}".format(sense, tile.coord))


def add_sense_tile(sense, tile):
    ent = sense.entity
    senses = tile.senses
    found = False
    for temp_sense in senses:
        if ent == temp_sense.entity:
            dist1 = sense.distances
            dist2 = temp_sense.distances
            # merge em!
            ndist = Distances
            ndist.sight = max(dist1.sight, dist2.sight)
            ndist.physical = min(dist1.physical, dist2.physical)
            ndist.hearing = min(dist1.hearing, dist2.hearing)
            nsense = Sense(ent, sense.pcoord, ndist)
            remove_sense_tile(temp_sense, tile)
            tile.senses.append(nsense)
            #print("Merging... new: {}".format(nsense))
            found = True
            break
    if not found:
        tile.senses.append(sense)
        #print("Adding... {}".format(sense))


dir_delta = {
    "n" : (0, 1),
    "ne" : (1, 1),
    "e" : (1, 0),
    "se" : (1, -1),
    "s" : (0, -1),
    "sw" : (-1, -1),
    "w" : (-1, 0),
    "nw" : (-1, 1)
}


def get_delta_distance(coord1, coord2):
    if ((coord1.x - coord2.x)**2 + (coord1.y - coord2.y)**2) == 1:
        new_dist = Distances(5, 5, 5)
    else:       # moving diagonally
        new_dist = Distances(7.5, 7.5, 7.5)
    return new_dist


def expand_sense_dir(world, start_sense, start_coord, main_dir, sub_dirs,
    dist_to_travel):
    dx, dy = dir_delta[main_dir]
    entity = start_sense.entity
    temp_coord = start_coord
    distance = start_sense.distances
    temp_sense = start_sense
    while distance.physical <= dist_to_travel:

        # handle sub_dirs now
        for direction in sub_dirs:
            expand_sense_dir(world, temp_sense, temp_coord, direction, [],
                dist_to_travel)

        pcoord = temp_coord
        new_coord = Coord(pcoord.x + dx, pcoord.y + dy)
        delta_distance = get_delta_distance(pcoord, new_coord)
        distance += delta_distance

        temp_sense = Sense(entity, pcoord, distance)
        tile = get_tile(world, new_coord)
        if tile:
            add_sense_tile(temp_sense, tile)
            temp_coord = new_coord
        else:
            break


def expand_out_senses(world, entity, dist_to_travel):
    # expand north
    start_sense = Sense(entity, entity.coord, Distances(0, 0, 0))
    expand_sense_dir(world, start_sense, entity.coord, "n", ["nw", "ne"],
        dist_to_travel)
    expand_sense_dir(world, start_sense, entity.coord, "e", ["se", "ne"],
        dist_to_travel)
    expand_sense_dir(world, start_sense, entity.coord, "s", ["se", "sw"],
        dist_to_travel)
    expand_sense_dir(world, start_sense, entity.coord, "w", ["nw", "sw"],
        dist_to_travel)


class Entity(object):
    def __init__(self, name, symbol, coord):
        self.name = name
        self.symbol = symbol
        self.coord = coord

    def __repr__(self):
        return "{} at {}".format(self.name, self.coord)


class Tile(object):
    def __init__(self, coord, distances, symbol="x"):
        self.symbol = symbol
        self.distances = distances
        self.coord = coord
        self.entities = []
        self.senses = []


def add_entity_tile(world, entity, coord):
    tile = get_tile(world, coord)
    tile.entities.append(entity)


class Region(object):
    def __init__(self, name):
        self.tiles = {}
        self.name = name
        self.entities = []


def display_map(radius, center, world):
    for y in range(center.y - radius, center.y + radius).__reversed__():
        line = []
        for x in range(center.x - radius, center.x + radius):
            coord = Coord(x, y)
            tile = get_tile(world, coord)
            if tile:
                symbol = get_symbol(tile)
            else:
                symbol = " "
            line.append(symbol)
        print("".join(line))


def get_entity_sense_tile(entity, tile):
    for sense in tile.senses:
        if sense.entity == entity:
            return sense


def get_sense_symbol(sense):
    distance = sense.distances.physical
    symbol = "s"
    if 0 <= distance < 10:
        symbol = "A"
    elif 10 <= distance < 20:
        symbol = "B"
    elif 20 <= distance < 30:
        symbol = "C"
    elif 30 <= distance < 40:
        symbol = "D"
    elif 40 <= distance < 50:
        symbol = "E"
    return symbol


def display_senses(radius, entity, world):
    cx, cy = entity.coord
    for y in range(cy - radius, cy + radius + 1).__reversed__():
        line = []
        for x in range(cx - radius, cx + radius + 1):
            coord = Coord(x, y)
            tile = get_tile(world, coord)
            if tile:
                sense = get_entity_sense_tile(entity, tile)
                if sense:
                    symbol = get_sense_symbol(sense)
                else:
                    symbol = "."
            else:
                symbol = " "
            line.append(symbol)
        print("".join(line))


def get_symbol(tile):
    symbol = tile.symbol
    for entity in tile.entities:
        symbol = entity.symbol
        break
    return symbol


def get_tile(world, coord):
    try:
        region = world[coord]
        tile = region.tiles[coord]
    except:
        tile = None
    return tile


def world_add_tile(world, region, tile):
    coord = tile.coord
    region.tiles[coord] = tile
    world[coord] = region


def  get_entities(world, coord):
    try:
        tile = get_tile(world, coord)
        entities = tile.entities
    except:
        entities = []
    return entities


def find_entities_range(world, center, radius):
    entities = []
    sx = center.x - radius
    ex = center.x + radius
    sy = center.x - radius
    ey = center.x + radius
    for coord in (Coord(tx, ty) for tx in range(sx, ex)
        for ty in range(sy, ey)):
        entities.extend(get_entities(world, coord))
    return entities


def make_region(name, start_coord, end_coord, world, spec_sym, def_sym):
    reg = Region(name)
    distances = Distances(2.5, 2.5, 2.5)
    for coord in (Coord(tx, ty) for tx in range(start_coord.x, end_coord.x)
        for ty in range(start_coord.y, end_coord.y)):

        if coord.x != coord.y:
            symbol = spec_sym
        else:
            symbol = def_sym
        new_tile = Tile(coord, distances, symbol)
        world_add_tile(world, reg, new_tile)


class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start


if __name__ == "__main__":
    
    default_tile = Tile(Coord(0, 0), Distances(3, 3, 3), "x")
    default_region = Region("bum")
    world = defaultdict(lambda: default_region)
    
    make_region("tomorrowland", Coord(-100, -100), Coord(100, 100), world,
        "1", "2")
    bob = Entity("bob", "B", Coord(1, 2))
    add_entity_tile(world, bob, bob.coord)
    tim = Entity("tim", "T", Coord(8, 2))
    add_entity_tile(world, tim, tim.coord)

    #display_map(12, 12, world)
    
    """
    ents = find_entities_range(world, bob.coord, 40)
    print("Entities in range: {}".format(ents))
    
    with Timer() as t:
        num = 1000
        for i in range(num):
            find_entities_range(world, bob.coord, 40)
    print("Time to run {} times: {} seconds".format(num, t.interval))
    """

    tile1 = get_tile(world, bob.coord)
    dist = Distances(5, 5, 5)
    sen = Sense(bob, bob.coord, dist)
    print(sen)
    #add_sense_tile(sen, tile1)
    #add_sense_tile(sen, tile1)
    expand_out_senses(world, bob, 100)
    display_senses(20, bob, world)
    print(bob)

    """
    with Timer() as t:
        num = 1000
        for i in range(num):
            expand_out_senses(world, bob, 60)
    print("Time to run {} times: {} seconds".format(num, t.interval))
    """
