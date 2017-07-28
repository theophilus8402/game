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

        self.special_effects = set()

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

    def apply_damage(self, dmg_info):
        """
        Given a DmgInfo object, with dmg info in it already, entity will
        check it's own resists and apply dmg as appropriate.  This function
        will be called by anything that can apply dmg (physical hit, spell cast,
        trap...)  Thus, I don't have to duplicate the searching for and applying
        of dmg resists in each of the other methods.
        Applies the dmg to the entities health.
        Returns the total amount of dmg applied to the entity.
        """
        # TODO: look for resists and apply them
        # resists can come from race, class, spells/special effects

        # apply the final amount
        # TODO: this may look different after I figure out resists
        final_amt = dmg_info.total

        self.cur_hp -= final_amt

        return final_amt


def get_block_value(item):
    # Returns the block value of an item, zero otherwise
    block_value = 0
    for effect in item.special_effects:
        if effect.spec_type is Effect.blocking:
            block_value = effect.block_value
            break
    return block_value


def entity_get_volume_weight(entity):
    """Returns the volume and weight of the entity."""
    return entity.volume, entity.weight
