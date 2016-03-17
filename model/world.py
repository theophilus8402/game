from copy import copy
from math import sqrt
import sys

import model.entity.entity
from model.info import Status
from model.tile import *

class World:

    def __init__(self):
        stdin = model.entity.entity.Entity()
        stdin.name = "stdin"
        stdin.sock = sys.stdin
        stdin.special_state = False
        stdin.state = None

        # key is the socket, value is the Entity
        self.sock_peeps = {}
        self.sock_peeps[sys.stdin] = stdin

        self.outputs = []
        self.passwds = {}        # key is name, passwd is value

        self.tiles = {}
        self.basic_ents = {}
        self.weapon_ents = {}
        self.armour_ents = {}
        self.living_ents = {}
        self.spells = {}

        # these max uids are the current highest uid
        # so, to create a new uid, return max_uid++
        self.max_tile_uid = 0
        self.max_ent_uid = 0

        self.msgs = []


    def add_msg(self, msg):
        self.msgs.append(msg)

    def remove_msg(self, msg):
        self.msgs.remove(msg)

    def run_msgs(self):
        for msg in self.msgs:
            if msg.check():
                recurring = msg.execute()
                if not recurring:
                    self.remove_msg(msg)

    def get_new_tile_uid(self):
        self.max_tile_uid += 1
        return self.max_tile_uid

    def get_new_ent_uid(self):
        self.max_ent_uid += 1
        return self.max_ent_uid

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


def distance_between_coords(coord1, coord2):
    """Returns the distance between two entities."""
    x1, y1 = coord1
    x2, y2 = coord2
    distance_squared = (x2 - x1)**2 + (y2 - y1)**2
    return sqrt(distance_squared)


def move_entity(world, entity, cur_loc, dst_loc):
    """
    Actually moves the entity from cur_loc to dst_loc.  This enables both the entity
    walking from one tile to another and some mechanism of teleporting to a different
    area in the world.
    Checks the area for new/old entities.
    TODO: May need to make more checks.  Currently, making a lot of assumptions.
    """
    cur_tile = get_tile(world, cur_loc)
    dst_tile = get_tile(world, dst_loc)

    # make sure entity is in cur_tile
    if entity in cur_tile.entities:

        # remove entity from cur_tile
        remove_entity(cur_tile, entity)

        # add entity to dest_tile
        add_entity(dst_tile, entity)

        dist_travelled = distance_between_coords(cur_loc, dst_loc)
        # if only moved a distance of once square
        if dist_travelled < 2:
            move_check_nearby_entities(world, entity, dst_loc - cur_loc)
        # if further, probably teleported and needs to check the area again
        else:
            area_entity_check(world, entity)


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



