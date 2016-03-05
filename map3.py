#!/usr/bin/python3

from copy import copy
from queue import Queue
from random import choice

from map import (Coord, Distances, make_region, Timer, get_tile, display_map, Entity,
    add_entity_tile, display_senses, get_entity_sense_tile)


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


def calculate_delta_distances(src_tile, dst_tile):
    delta_coord = dst_tile.coord - src_tile.coord
    #print("delta_coord: {}".format(delta_coord))
    physical = get_delta_distance(delta_coord)
    hearing = 5
    sight = 5
    return Distances(physical, hearing, sight)


def saw_someone(entity1, entity2):
    # yep, add the peeps, both ways
    # the entities are within visual range of each other and need to be added
    #   to entity.peeps_nearby
    """
    print("Adding {} and {} to each other's peeps_nearby set.".format(entity1.name,
        entity2.name))
    """
    entity1.peeps_nearby.add(entity2)
    entity2.peeps_nearby.add(entity1)
    pass


def lost_someone(entity1, entity2):
    # the entities moved out of visual range from each other
    """
    print("Removing {} and {} from each other's peeps_nearby set.".format(entity1.name,
        entity2.name))
    """
    entity1.peeps_nearby.discard(entity2)
    entity2.peeps_nearby.discard(entity1)


def check_tile_new_entity(world, coord, searching_entity):
    temp_tile = get_tile(world, coord)
    if temp_tile:
        new_entities = []
        for ent in temp_tile.entities:
            if ent.name != searching_entity.name:
                saw_someone(searching_entity, ent)
                #print("Saw {} at {}.".format(ent.name, coord))


def check_entities_out_of_range(entity, check_x, check_y):
    #print("Check out of range: ({}, {})".format(check_x, check_y))
    peeps = copy(entity.peeps_nearby)
    for ent in peeps:
        temp_x, temp_y = ent.coord
        if check_x != None and temp_x == check_x:
            lost_someone(entity, ent)
        elif check_y != None and temp_y == check_y:
            lost_someone(entity, ent)


def initial_check(world, entity):
    # look in the area for people to add
    vrange = entity.visual_range
    center_x, center_y = entity.coord
    for y in range(center_y - vrange, center_y + vrange + 1).__reversed__():
        for x in range(center_x - vrange, center_x + vrange + 1):
            #print("initial_check at {}".format(Coord(x, y)))
            check_tile_new_entity(world, Coord(x, y), entity)

# this will be called after the entity has been moved
def move_check(world, entity, coord_delta):
    delta_x, delta_y = coord_delta
    center_x, center_y = entity.coord
    visual_range = entity.visual_range
    # need to check both because we may move diagonally
    if delta_x:
        # fix x and search along the y-axis
        new_x = center_x + delta_x*visual_range
        old_x = center_x - delta_x*(visual_range + 1)

        # look for new entities to add
        for temp_y in range(center_y - visual_range, center_y + visual_range + 1):
            #print("move_check at {}".format(Coord(new_x, temp_y)))
            check_tile_new_entity(world, Coord(new_x, temp_y), entity)

        # look for entities no longer in view to remove
        check_entities_out_of_range(entity, old_x, None)

    if delta_y:
        # fix y and search along the x-axis
        new_y = center_y + delta_y*visual_range
        old_y = center_y - delta_y*(visual_range + 1)

        # look for new entities to add
        for temp_x in range(center_x - visual_range, center_x + visual_range + 1):
            #print("move_check at {}".format(Coord(temp_x, new_y)))
            check_tile_new_entity(world, Coord(temp_x, new_y), entity)

        # look for entities no longer in view to remove
        check_entities_out_of_range(entity, None, old_y)


# this is the base move action
def move(world, entity, dst_tile):

    # remove the entity from the current tile
    cur_tile = get_tile(world, entity.coord)
    cur_tile.entities.remove(entity)

    # add entity to the new tile
    dst_tile.entities.append(entity)

    # update entity's coord
    entity.coord = dst_tile.coord


# this is called when the user initiates a move
def action_move(world, entity, move_dir):

    coord_delta = dir_delta[move_dir]
    dst_tile = get_tile(world, entity.coord + coord_delta)

    if dst_tile:
        # actually move the entity
        move(world, entity, dst_tile)
    
        # update entities in visual range
        #print("Now at: {}".format(entity.coord))
        move_check(world, entity, coord_delta)


# TODO: Rework display_map() to take into account peeps that the entity sees


if __name__ == "__main__":

    world = {}

    make_region("Snowland", Coord(-300, -300), Coord(300, 3000), world, ".", "*")
    print("Number of rooms: {}".format(len(world.keys())))

    bob = Entity("bob", "B", Coord(1, 1))
    bob.visual_range = 30
    tim = Entity("tim", "T", Coord(3, 8))
    jon = Entity("jon", "J", Coord(-1, -1))

    bob_tile = get_tile(world, bob.coord)
    bob_tile.entities.append(bob)
    tim_tile = get_tile(world, tim.coord)
    tim_tile.entities.append(tim)
    jon_tile = get_tile(world, jon.coord)
    jon_tile.entities.append(jon)

    #saw_someone(bob, tim)
    #lost_someone(bob, tim)

    #display_map(10, bob.coord, world)

    initial_check(world, bob)

    peeps = []
    num_peeps = 10
    for i in range(num_peeps):
        new_coord = choice(list(world.keys()))
        new_entity = Entity("bob{}".format(i), "b", new_coord)
        new_entity.visual_range = 30
        entity_tile = get_tile(world, new_coord)
        entity_tile.entities.append(new_entity)
        initial_check(world, new_entity)
        peeps.append(new_entity)
        print("Creating: {}...".format(new_entity))

    """
    dir_list = list(dir_delta.keys())
    for i in range(5):
        move_dir = choice(dir_list)
        print("\nMoving '{}'...".format(move_dir))
        action_move(world, bob, move_dir)
    
    #TODO: test how long it takes to do 100,000
    """
    print("\nStart timer...")
    num_times = 100000
    with Timer() as t:
        dir_list = list(dir_delta.keys())
        for i in range(num_times):
            move_dir = choice(dir_list)
            #print("\nMoving '{}'...".format(move_dir))
            action_move(world, bob, move_dir)
    print("Time to run {} times: {} seconds".format(num_times, t.interval))



    print("\nNearby peeps:")
    print(bob.peeps_nearby)
    print(tim.peeps_nearby)
    print(jon.peeps_nearby)
