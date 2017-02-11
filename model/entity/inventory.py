#!/usr/bin/python3

from model.info import Status
from model.entity.basic_entity import entity_get_volume_weight

class Inventory():
    """
    The inventory is something that is meant to be flexible.  It can be used
    for the entities actual inventory or it can be an inventory within a container
    (i.e. a backpack or chest).
    """

    def __init__(self, volume_capacity=20, weight_capacity=30):
        self._items = {}
        self.volume_capacity = volume_capacity
        self.weight_capacity = weight_capacity
        self.current_items_volume = 0
        self.current_items_weight = 0

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        return item in self._items.values()

    def add_item(self, item):
        self._items[item.name.lower()] = item
        volume, weight = entity_get_volume_weight(item)
        self.current_items_volume += volume
        self.current_items_weight += weight

    def can_add_item(self, item):
        """
        Returns Status.all_good if item can fit,
        Status.item_too_big if it doesn't fit by volume,
        Status.item_too_heave if it doesn't fit by weight.
        """
        volume, weight = entity_get_volume_weight(item)
        can_add = Status.all_good
        if (volume + self.current_items_volume) > self.volume_capacity:
            can_add = Status.item_too_big
        elif (weight + self.current_items_weight) > self.weight_capacity:
            can_add = Status.item_too_heavy
        return can_add

    def remove(self, item):
        """
        Removes the item from the inventory.  Reduces the inventory's
        current_items_volume/weight as appropriate.
        """
        item_found = self._items.pop(item.name.lower(), False)
        if item_found:
            item_found = True
            volume, weight = entity_get_volume_weight(item)
            self.current_items_volume -= volume
            self.current_items_weight -= weight
        return item_found


    def find_item(self, name):
        """
        Returns an item if its name or a keyword match the supplied name.
        Returns None otherwise.
        """
        # this might be a generic name like sword, or more specific i.e. sword99
        # first look to see if we can find it by it's name
        item = self._items.get(name.lower())

        # then, look through keywords of the name
        if not item:
            #TODO!!  maybe add something to item to see if name describes it
            pass
        return item


def inventory_get_items(inventory):
    """Returns a set of items currently in the inventory."""
    return set(inventory.items.values())


def inventory_get_current_capacity(inventory):
    """
    Returns a tuple consisting of (volume, weight).  The volume and weight are
    the sum total of all the items in the inventory volume and weight.
    """
    return inventory.current_items_volume, inventory.current_items_weight

