#!/usr/bin/python3

from queue import Queue

from map import (Coord, Distances, make_region, Timer, get_tile, display_map, Entity,
    add_entity_tile, remove_sense_tile, display_senses, get_entity_sense_tile)

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
    entity.senses.append(sense)


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


def get_delta_distance(delta_coord):
    if delta_coord in [Coord(1, 1), Coord(1, -1), Coord(-1, -1), Coord(-1, 1)]:
        distance = 7.5
    else:
        distance = 5
    return distance


def remove_sense_tile(sense, tile):
    tile.senses.remove(sense)
    entity = sense.entity
    entity.senses.remove(sense)


def expand_sense(world, start_sense, delta_coords, distance_to_travel):
    """
    This will take a single sense and expand it out one level in all directions we're
    told to go (delta_coords). This will test if we've gone too far, if there's
    already a sense there, determine which should stay, change parents/children when
    appropriate. At the end of expanding out the sense, we will return a list of all
    newly created and still valid senses so that they can be queued and then expanded
    out by expand_out_senses().
    """
    new_senses = []
    entity = start_sense.entity
    start_coord = start_sense.coord
    #print("base_coord: {}".format(start_sense.coord))
    for delta_coord in delta_coords:
        new_coord = start_coord + delta_coord
        #print("new_coord: {}".format(new_coord))

        tile = get_tile(world, new_coord)    # make sure the tile exists
        if not tile:
            continue

        delta_distance = get_delta_distance(delta_coord)
        new_distances = start_sense.distances + Distances(delta_distance, 0, 0)
        if distance_to_travel < new_distances.physical:
            continue     # make sure we haven't travelled too far

        
        new_sense = Sense(entity, start_coord, new_coord, new_distances)

        tile_sense = get_entity_sense_tile(entity, tile)
        if tile_sense:   # check if there's a sense already there
            if new_distances.physical < tile_sense.distances.physical:    # shorter
                remove_sense_tile(tile_sense, tile)
            else:
                continue    # new_sense is longer, so, not adding it

        add_sense_tile(new_sense, tile) # if we're here, should add the sense
        new_senses.append(new_sense)
    return new_senses


def expand_out_senses(world, entity, dist_to_travel):
    """
    Let's keep things "simple". So, we're going to expand out senses only once each
    time the entity get's added to the world. We're not going to calculate distances
    for hearing and sight. We'll calculate after we expand. We'll also expand in all
    directions. This will let us try to find the actual shortest path. Along the way,
    we will keep track of parents and children.
    """
    start_sense = Sense(entity, None, entity.coord, Distances(0, 0, 0))
    add_sense_entity(start_sense, entity)
    add_sense_tile(start_sense, get_tile(world, entity.coord))

    dir_deltas = dir_delta.values()

    sense_queue = Queue()
    sense_queue.put(start_sense)
    while not sense_queue.empty():
        sense = sense_queue.get()
        children = expand_sense(world, sense, dir_deltas, dist_to_travel)
        #print("new_senses: {}".format(children))
        sense.children = children
        entity.senses.extend(children)
        for child in children:
            sense_queue.put(child)


if __name__ == "__main__":

    world = {}

    make_region("Snowland", Coord(-20, -20), Coord(20, 20), world, ".", "*")

    bob = Entity("bob", "B", Coord(1, 2))
    bob.senses = []
    add_entity_tile(world, bob, bob.coord)
    display_map(10, bob.coord, world)

    sen1 = Sense(bob, None, bob.coord, Distances(0, 0, 0))
    bob_tile = get_tile(world, bob.coord)
    #add_sense_tile(sen1, bob_tile)
    #add_sense_entity(sen1, bob)
    display_senses(5, bob, world)
    #move_all_senses(world, bob, "n")
    print("\nExpanding senses...")
    expand_out_senses(world, bob, 14)
    display_senses(15, bob, world)

    print("Bob's senses:")
    print(len(bob.senses))
    #print(bob.senses[0])
