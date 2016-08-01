#!/usr/bin/python3


def change_hp(entity, hp_delta):
    """Changes entity's HP by the given amount.  Doesn't return anything."""
    entity.cur_hp += hp_delta


# Most basic class:
class Entity:

    def __init__(self, cur_hp=0):
        # stuff stored in db in order
        self.uid = 0 # TODO: implement this more
        self.name = None
        self.type = "entity"      # the different entity classes
        self.symbol = ""
        self.coord = (0, 0)
        self.cur_hp = 0
        self.max_hp = 10

        self.short_desc = ""
        self.long_desc = ""
        self.weight = 0
        self.volume = 0  # this is how we will block movement
                         # a 5ftx5ftx10ft room is a max 250ft^3
        self.friction = 0

        #TODO: probably gonna change it so peeps_nearby is only in living entities
        self.peeps_nearby = set()

        # stuff not stored in db
        self.world = None


def entity_get_volume_weight(entity):
    """Returns the volume and weight of the entity."""
    return entity.volume, entity.weight
