#!/usr/bin/python3

dir_coord_changes = {
    "n" : (0, 1),
    "ne" : (1, 1),
    "e" : (1, 0),
    "se" : (1, -1),
    "s" : (0, -1),
    "sw" : (-1, -1),
    "w" : (-1, 0),
    "nw" : (-1, 1)
}


def expand_sense_once(world, sense):
    """
    Figure things out for the next iteration of tiles
        Different distances: sight and hearing
        sight can't travel through walls or other similar obstructions
        so, for sight, we will keep the highest sight number
        hearing can, but will be impeded by walls and other obstructions
        so, for hearing, we will keep the lowest because sound travels around things
    """
    src_tile = world.tiles[sense.coord]
    cur_x, cur_y = sense.coord
    new_senses = []
    for direction in sense.directions_to_travel:
        delta_x, delta_y = dir_coord_changes[direction]
        new_coord = (cur_x + delta_x, cur_y + delta_y)
        # make sure the room exists
        try:
            dest_tile = world.tiles[new_coord]
        except:
            continue # room doesn't exist

        # figure out the distance from this tile to the next
        total = sense.distance_travelled + src_tile.distances[direction]["physical"]
        if total > sense.total_distance_to_go:
            continue

        new_hearing_dist = (sense.hearing_distance +
            src_tile.distances[direction]["hearing"])
        new_sight_dist = (sense.sight_distance +
            src_tiles.distances[direction]["sight"])

        # add/merge the sense object to the dest_tile
        new_sense = add_sense_tile(coord=new_coord, travelled=total,
            total=total_distance_to_go, entity=sense.entity, dirs=sense.dirs,
            sdist=new_sight_distance, hdist=new_hearing_dist, pcoord=sense.coord)

        new_senses.append(new_sense)
    return new_senses


def add_sense_tile(coord=(0, 0), travelled=0, total=0, entity=None, dirs=list(),
    sdist=0, hdist=0, pcoord=(0, 0)):
    """
    Adds or merges a "sense" object to the tile.  If a sense object already exists for
    the given entity, we will merge the objects.  To do this, we will keep the
    higheset sight and the least hearing.
    """


def expand_all_senses():
    """
    Expands everything for the given entity.
    Continues to loop until all the sense objects can't expand any more.
    """
    pass


Class Sense(BaseObject):

    def __init__(self, coord=(0, 0), travelled=0, total=0, entity=None, dirs=list(),
        sdist=0, hdist=0, pcoord=(0, 0)):
        self.distance_travelled = travelled     # physical distance
        self.total_distance_to_go = total       # physical distance
        self.hearing = (hdist, pcoord)
        self.sight = (sdist, pcoord)            # they might have diff pcoords
        self.entity = entity
        self.directions_to_travel = dirs
        self.coord = coord
