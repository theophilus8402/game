
from collections import namedtuple


class InvalidCoords(Exception):
    pass

class CoordsOccupied(Exception):
    pass


Transaction = namedtuple("Transaction", ["action", "input"])


def set_map(world, map_input):
    x_len = len(world.x_range)
    y_len = len(world.y_range)
    for y,yi in zip(list(world.y_range), list(range(y_len-1, -1, -1))):
        for x,xi in zip(list(world.x_range), list(range(x_len))):
            #print("{}, {}".format((x, y), (xi, yi)))
            piece = map_input[yi][xi]
            piece = piece if piece != "." else None
            world.map[(x, y)] = piece


def display_map(world):
    for y in world.y_range.__reversed__():
        row = []
        for x in world.x_range:
            piece = world.map[(x, y)]
            piece = piece if piece else "."
            #print("{}, {}".format((x, y), (xi, yi)))
            row.append(piece)
        print("".join(row))


def generate_map(x_range=range(-1, 2), y_range=range(-1, 2)):
    game_map = {}
    for x in x_range:
        for y in y_range:
            game_map[(x, y)] = None
    return game_map


class World():

    def __init__(self, game_id=0, x_range=range(-1, 2), y_range=range(-1, 2)):
        self.game_id = game_id
        self.x_range = x_range
        self.y_range = y_range
        self.map = generate_map(x_range=self.x_range, y_range=self.y_range)

        self.transaction_actions = {
            "set_piece": (self.set_piece, self.undo_set_piece),
        }

    def set_piece(self, piece, coords):
        # places the specified piece in specified coords
        # if self.map[coords] is already occupied,
        # raises an CoordsOccupied exception
        # if invalid coords are provided, raises InvalidCoords exception

        # make sure they're valid coords
        if coords not in self.map.keys():
            raise InvalidCoords()

        # make sure the coords aren't already occupied
        if self.map[coords]:
            raise CoordsOccupied

        self.map[coords] = piece

    def undo_set_piece(self, piece, coords):
        # removes the piece from the specified coords

        # make sure they're valid coords
        if coords not in self.map.keys():
            raise InvalidCoords()

        self.map[coords] = None

    def apply_transaction(self, trans):

        action,undo_action = self.transaction_actions[trans.action]

        #import pdb;pdb.set_trace()
        action(**trans.input)

    def undo_transaction(self, trans):

        action,undo_action = self.transaction_actions[trans.action]

        undo_action(**trans.input)

    @property
    def winner(self):
        # Returns the winning piece, if there's a winner
        # Returns None, if there's no winner

        # check for horizontal wins
        for y in self.y_range:
            row = set()
            for x in self.x_range:
                row.add(self.map[(x, y)])
            if (len(row) == 1) and (row != {None}):
                return row.pop()

        # check for vertical wins
        for x in self.x_range:
            col = set()
            for y in self.y_range:
                col.add(self.map[(x, y)])
            if (len(col) == 1) and (col != {None}):
                return col.pop()

        # check for diagonal wins
        diag1 = {self.map[(i, -i)] for i in self.x_range}
        diag2 = {self.map[(-i, -i)] for i in self.x_range}
        for diag in [diag1, diag2]:
            if (len(diag) == 1) and (diag != {None}):
                return diag.pop()

        return None

    @property
    def game_over(self):
        # Returns True, if there's a winner or all spots are filled
        # Returns False otherwise

        if self.winner:
            return True

        for symbol in self.map.values():
            if not symbol:
                return False

        return True

