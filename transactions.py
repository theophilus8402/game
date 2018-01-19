
from collections import namedtuple

Coord = namedtuple("Coord", ["x", "y"])
Transaction = namedtuple("Transaction", [
                            "entity",
                            "source",
                            "reason",
                            "function",
                            "delta"])


dir_coords = {
    "n": Coord(0, 1),
    "e": Coord(1, 0),
    "s": Coord(0, -1),
    "w": Coord(-1, 0),
}


def delta_location(world, transaction):
    entity = world.entities[transaction.entity.lower()]
    world.transactions.append(transaction)
    current_coords = entity.coords
    del(world.map[current_coords])
    dx, dy = dir_coords[transaction.delta]
    new_coords = Coord(current_coords.x+dx, current_coords.y+dy)
    world.map[new_coords] = entity
    entity.coords = new_coords


def undo_delta_location(world, transaction):
    entity = world.entities[transaction.entity.lower()]
    #world.transactions.append(transaction)
    current_coords = entity.coords
    del(world.map[current_coords])
    dx, dy = dir_coords[transaction.delta]
    old_coords = Coord(current_coords.x-dx, current_coords.y-dy)
    world.map[old_coords] = entity
    entity.coords = old_coords


def set_location(world, transaction):
    entity = world.entities[transaction.entity.lower()]
    world.transactions.append(transaction)
    original_coords, coords = transaction.delta
    if original_coords:
        del(world.map[original_coords])
    world.map[coords] = entity
    entity.coords = coords


def undo_set_location(world, transaction):
    entity = world.entities[transaction.entity.lower()]
    #world.transactions.append(transaction)
    original_coords, coords = transaction.delta
    del(world.map[coords])
    if original_coords:
        world.map[original_coords] = entity
    entity.coords = original_coords


class World():

    def __init__(self):
        self.entities = {}
        self.map = {}
        self.transactions = []
        self.transaction_functions = {
            "set_location": (set_location, undo_set_location),
            "delta_location": (delta_location, undo_delta_location),
        }

    def add_entity(self, entity):
        self.entities[entity.name.lower()] = entity

    def apply_transaction(self, transaction):
        self.transaction_functions[transaction.function][0](self, transaction)

    def undo_transaction(self, transaction):
        self.transaction_functions[transaction.function][1](self, transaction)


class Entity():

    def __init__(self, name):
        self.name = name
        self.coords = Coord(0, 0)
        self.bonuses = set()
        self.hp = 10
        self.xp = 0


if __name__ == "__main__":

    world = World()
    bob = Entity("Bob")
    world.add_entity(bob)

    trans1 = Transaction("bob", "world", "initial_placement", "set_location", 
                            (None, Coord(1, 1)))
    trans2 = Transaction("bob", "world", "move", "delta_location", "n")

    import pdb;pdb.set_trace()
    world.apply_transaction(trans1)
    world.apply_transaction(trans2)
    world.undo_transaction(trans2)
    world.undo_transaction(trans1)

