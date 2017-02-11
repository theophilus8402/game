from copy import copy
from math import sqrt
import sys

from model.info import Status, Coord
from model.tile import *
from model.util import distance_between_coords

class World:

    def __init__(self):
        self.tiles = {}
        self.basic_ents = {}
        self.weapon_ents = {}
        self.armour_ents = {}
        self.living_ents = {}
        self.spells = {}
        self.socket_entity_map = {}
        self.ai_entities = []
        self.actions = None
        self.server_socket = None

        # these max uids are the current highest uid
        # so, to create a new uid, return max_uid++
        self.max_tile_uid = 0
        self.max_ent_uid = 0

    def find_entity(self, name):
        name = name.lower()
        entity = self.living_ents.get(name)
        if not entity:
            entity = self.weapon_ents.get(name)
        if not entity:
            entity = self.armour_ents.get(name)
        if not entity:
            entity = self.basic_ents.get(name)
        return entity


def move_entity(world, entity, dst_loc):
    """
    Actually moves the entity from cur_loc to dst_loc.  This enables both the entity
    walking from one tile to another and some mechanism of teleporting to a different
    area in the world.
    Checks the area for new/old entities.
    TODO: May need to make more checks.  Currently, making a lot of assumptions.
    """
    cur_loc = entity.coord
    cur_tile = get_tile(world, cur_loc)
    dst_tile = get_tile(world, dst_loc)

    status = Status.all_good

    if not dst_tile:
        status = Status.tile_doesnt_exist

    # make sure entity is in cur_tile
    if ((status == Status.all_good) and (entity in cur_tile.entities)):

        # remove entity from cur_tile
        tile_remove_entity(cur_tile, entity)

        # add entity to dest_tile
        tile_add_entity(dst_tile, entity)

        # update peeps_nearby
        dist_travelled = distance_between_coords(cur_loc, dst_loc)
        # if only moved a distance of one square
        if dist_travelled < 2:
            move_check_nearby_entities(world, entity, cur_loc-dst_loc)
            #print("running move_check_nearby: {}".format(cur_loc-dst_loc))
        # if further, probably teleported and needs to check the area again
        else:
            area_entity_check(world, entity)

    return status


# this will be called after the entity has been moved
def move_check_nearby_entities(world, entity, coord_delta):
    """
    Checks the surrounding area within the entity's visual_range for new entities.
    If new entities are found, they're added to the list of nearby_peeps.
    It only does a partial check checking only the newest tiles within visual_range.
    It also checks to see if any entities left this entity's visual range and removes
    them from the list.  It only checks coords which are no longer in range.
    """
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
            #print("move_check_nearby_entities at {}".format(Coord(new_x, temp_y)))
            tmp_tile = get_tile(world, Coord(new_x, temp_y))
            try:
                check_tile_new_entity(tmp_tile, entity)
            except:
                #print("The coord, {}, doesn't exist!".format(Coord(new_x, temp_y)))
                pass

        # look for entities no longer in view to remove
        check_entities_out_of_range(entity, old_x, None)

    if delta_y:
        # fix y and search along the x-axis
        new_y = center_y + delta_y*visual_range
        old_y = center_y - delta_y*(visual_range + 1)

        # look for new entities to add
        for temp_x in range(center_x - visual_range, center_x + visual_range + 1):
            #print("move_check_nearby_entities at {}".format(Coord(temp_x, new_y)))
            tmp_tile = get_tile(world, Coord(temp_x, new_y))
            try:
                check_tile_new_entity(tmp_tile, entity)
            except:
                #print("The coord, {}, doesn't exist!".format(Coord(temp_x, new_y)))
                pass

        # look for entities no longer in view to remove
        check_entities_out_of_range(entity, None, old_y)


def get_tile(world, coord):
    """Returns the tile at the given coord.  Returns None, if tile doesn't exist."""
    return world.tiles.get(coord)


def area_entity_check(world, entity):
    """Checks for entities in the area to add to each other's peeps_nearby lists."""
    entity.peeps_nearby.clear()
    # look in the area for people to add
    vrange = entity.visual_range
    center_x, center_y = entity.coord
    for y in range(center_y - vrange, center_y + vrange + 1).__reversed__():
        for x in range(center_x - vrange, center_x + vrange + 1):
            #print("initial_check at {}".format(Coord(x, y)))
            tmp_tile = get_tile(world, Coord(x, y))
            try:
                check_tile_new_entity(tmp_tile, entity)
            except:
                # the tile doesn't exist, so don't do anything
                pass


def check_entities_out_of_range(entity, check_x, check_y):
    """
    Removes entities from each other's list of peeps_nearby that are now
    out-of-range because of a move.
    """
    #print("Check out of range: ({}, {})".format(check_x, check_y))
    peeps = copy(entity.peeps_nearby)
    for ent in peeps:
        temp_x, temp_y = ent.coord
        if ((check_x != None and temp_x == check_x) or
            (check_y != None and temp_y == check_y)):
            entity.peeps_nearby.discard(ent)
            ent.peeps_nearby.discard(entity)


def entities_within_distance(center_coord, entities, distance):
    """
    Takes a center_coord, a list of entities, and a distance.
    It tests each entity to see if it's close enough to the center_coord.
    If so, the entity get's appended to a new list which is returned
    at the end of the function.  Defaults to sending an empty list.
    """
    ents_within_distance = []
    for entity in entities:
        if distance_between_coords(center_coord, entity.coord) <= distance:
            ents_within_distance.append(entity)
    return ents_within_distance


def world_add_entity(world, entity):
    """
    Adds the entity to the world.  Adds the entity to the appropriate tile and the
    appropriate list of entities within the world.
    """
    tile = get_tile(world, entity.coord)
    tile_add_entity(tile, entity)
    input_handle = entity.comms.get_input_handle()
    world.socket_entity_map[input_handle] = entity
    if isinstance(entity, Living):
        #world.living_ents[entity.name.lower()] = entity
        area_entity_check(world, entity)
    else:
        #TODO: add the other types
        pass
