#!/usr/bin/python3

from map import (Coord, Distances, make_region, Timer, get_tile, display_map, Entity,
    add_entity_tile, remove_sense_tile, display_senses)

class Sense(object):
    def __init__(self, entity, psense, coord, distances):
        self.entity = entity
        self.parent = psense
        self.children = []
        self.coord = coord
        self.distances = distances

    def __repr__(self):
        return "{} : {}/{}/{}  {} -> -> {}".format(self.entity.name,
            self.distances.physical, self.distances.hearing,
            self.distances.sight, self.parent, self.children)


def add_children_sense(children, sense):
    sense.children.extend(children)


def add_sense_tile(sense, tile):
    tile.senses.append(sense)


def add_sense_entity(sense, entity):
    entity.senses.append(entity)


def move_sense(world, sense, src_tile, dir_delta):
    dst_coord = src_tile.coord + dir_delta
    dst_tile = get_tile(world, dst_coord)

    add_sense_tile(sense, dst_tile)
    remove_sense_tile(sense, src_tile)


dir_delta = {
    "n" : Coord(0, 1),
    "ne" : Coord(1, 1),
    "e" : Coord(1, 0),
    "se" : Coord(1, -1),
    "s" : Coord(0, -1),
    "sw" : Coord(-1, -1),
    "w" : Coord(-1, 0),
    "nw" : Coord(-1, 1)
}


def move_all_senses(world, entity, direction):
    src_tile = get_tile(world, entity.coord)
    delta = dir_delta[direction]
    for sense in entity.senses:
        move_sense(world, sense, src_tile, delta)


#def expand_sense_dir(world, start_sense, main_dir, sub_dirs


def expand_out_senses(world, entity, dist_to_travel):
    start_sense = Sense(entity, None, entity.coord, Distances(0, 0, 0))
    add_sense_entity(sense, entity)


if __name__ == "__main__":

    world = {}

    make_region("Snowland", Coord(0, 0), Coord(20, 20), world, ".", "*")

    bob = Entity("bob", "B", Coord(1, 2))
    bob.senses = []
    add_entity_tile(world, bob, bob.coord)
    display_map(10, 10, world)

    sen1 = Sense(bob, None, bob.coord, Distances(0, 0, 0))
    bob_tile = get_tile(world, bob.coord)
    add_sense_tile(sen1, bob_tile)
    add_sense_entity(sen1, bob)
    display_senses(1, bob, world)
    move_all_senses(world, bob, "n")
    print("")
    display_senses(1, bob, world)
