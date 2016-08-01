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
        self.items = {}
        self.volume_capacity = volume_capacity
        self.weight_capacity = weight_capacity
        self.current_items_volume = 0
        self.current_items_weight = 0


def inventory_get_items(inventory):
    """Returns a set of items currently in the inventory."""
    return set(inventory.items.values())


def inventory_get_current_capacity(inventory):
    """
    Returns a tuple consisting of (volume, weight).  The volume and weight are
    the sum total of all the items in the inventory volume and weight.
    """
    return inventory.current_items_volume, inventory.current_items_weight


def inventory_can_add_item(inventory, item):
    """
    Returns information about the ability to fit the given item in the inventory.
    Returns Status.all_good if the item can fit.
    Returns Status.item_too_big if the item is to voluminous.
    Returns Status.item_too_heavy if the item is too heavy for the inventory.
    """
    volume, weight = entity_get_volume_weight(item)
    status = Status.all_good
    if (volume + inventory.current_items_volume) > inventory.volume_capacity:
        status = Status.item_too_big
    elif (weight + inventory.current_items_weight) > inventory.weight_capacity:
        status = Status.item_too_heavy
    return status


def inventory_add_item(inventory, item):
    """
    Adds the item to the inventory.  Does not check capacities.  Increases
    the inventory's current_items_volume/weight as appropriate.
    """
    status = Status.all_good
    inventory.items[item.name.lower()] = item
    volume, weight = entity_get_volume_weight(item)
    inventory.current_items_volume += volume
    inventory.current_items_weight += weight
    return status


def inventory_remove_item(inventory, item):
    """
    Removes the item from the inventory.  Reduces the inventory's
    current_items_volume/weight as appropriate.
    """
    status = inventory.items.pop(item.name.lower(), None)
    if status == None:
        status = Status.target_doesnt_exist
    else:
        status = Status.all_good
        volume, weight = entity_get_volume_weight(item)
        inventory.current_items_volume -= volume
        inventory.current_items_weight -= weight
    return status


def inventory_find_item(inventory, name):
    """
    Returns an item based on a given name.  Returns None if no item found with
    that name.
    """
    return inventory.items.get(name.lower(), None)

