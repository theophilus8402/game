
from world import World

# to test things from the barebones user interface:
# server;bob;login
# server;bob;create,world1
# world1;bob;(1, 0)
# server;tim;login
# server;tim;join,world1
# world1;tim;(1, 1)
# world1;tim;undo
# server;kevin;login
# server;kevin;watch,world1


class Player():

    known = 0

    def __init__(self, name=None):

        if name:
            self.name = name
        else:
            self.name = "unknown{}".format(Player.known)
            Player.known += 1

        self.connection = None
        self.piece = None
        self.world = None


# class Observer():
#
#   def __init__():
#       self.connection
#       self.world
#       self.name


class WorldExists(Exception):
    def __init__(self, msg, game_id):
        self.message = msg
        self.game_id = game_id

class WorldDoesNotExist(Exception):
    def __init__(self, msg, game_id):
        self.message = msg
        self.game_id = game_id

class ConnectionExists(Exception):
    def __init__(self, msg, connection):
        self.message = msg
        self.connection = connection

class ConnectionDoesNotExist(Exception):
    def __init__(self, msg, connection):
        self.message = msg
        self.connection = connection

class NameExists(Exception):
    def __init__(self, msg, name):
        self.message = msg
        self.name = name

class NameDoesNotExist(Exception):
    def __init__(self, msg, name):
        self.message = msg
        self.name = name


class Interactor():

    def __init__(self):

        # self.worlds = {name : World}
        self.worlds = {}

        # self.players = {name : Player}
        self._players = {}

        # self.connections = {connection : Player}
        self.connections = {}

    @property
    def players(self, name):
        try:
            return self._players[name.lower()]
        except KeyError:
            raise NameDoesNotExist(
                "A Player with the name {} does not exist.".format(name),
                name)

    @players.setter
    def players(self, name, player):
        if lower_name not in self._players.keys():
            self._players[lower_name] = Player(name)
        else:
            raise NameExists(
                "A Player with the name, {}, already exists.".format(name),
                name)

    def apply_transaction(self, trans):

        action,undo_action = self.transaction_actions[trans.action]
        action(**trans.input)

    def create_world(self, game_id):

        # creates the world with the associated name and enters it into
        #   self.worlds

        if game_id not in self.worlds.keys():
            new_world = World(game_id=game_id)
            self.worlds[game_id] = new_world
        else:
            raise WorldExists(
                "A world already exists with game_id: {}".format(game_id),
                game_id)
        
    def undo_create_world(self, game_id):

        # undoes the creation of the specified world
        # raises a WorldDoesNotExist error if game_id doesn't exist

        try:
            del(self.worlds[game_id])
        except KeyError:
            raise WorldDoesNotExist(
                "World with game_id {} doesn't exist.".format(game_id),
                game_id)

    def create_player(self, name):

        lower_name = name.lower()

        if lower_name not in self.players.keys():
            self.players[lower_name] = Player(name)
        else:
            raise NameExists(
                "A Player with the name, {}, already exists.".format(name),
                name)

    def undo_create_player(self, name):

        try:
            del(self.players[name.lower()])
        except KeyError:
            raise NameDoesNotExist(
                "A Player with the name {} does not exist.".format(name),
                name)

    def change_connection(self, name, old_connection, new_connection):

        # find the player
        try:
            player = self.players[name.lower()]
        except KeyError:
            raise NameDoesNotExist(
                "A Player with the name {} does not exist.".format(name),
                name)

        # make sure this new_connection doesn't already exist
        if new_connection and new_connection in self.connections.keys():
            raise ConnectionExists(
                "A connection, {}, already exists.".format(new_connection),
                new_connection)

        # change the self.connections entries as appropriate
        try:
            del(self.connections[old_connection])
        except KeyError:
            if old_connection:
                raise ConnectionDoesNotExist(
                    "Connection, {}, doesn't exist.".format(old_connection),
                    old_connection)

        # set the connection
        player.connection = new_connection
        if new_connection:
            self.connections[new_connection] = player

    def undo_change_connection(self, name, old_connection, new_connection):

        # find the player
        try:
            player = self.players[name.lower()]
        except KeyError:
            raise NameDoesNotExist(
                "A Player with the name {} does not exist.".format(name),
                name)

        # make sure this new_connection doesn't already exist
        if old_connection and old_connection in self.connections.keys():
            raise ConnectionExists(
                "A connection, {}, already exists.".format(old_connection),
                old_connection)

        # change the self.connections entries as appropriate
        try:
            del(self.connections[new_connection])
        except KeyError:
            if new_connection:
                raise ConnectionDoesNotExist(
                    "Connection, {}, doesn't exist.".format(new_connection),
                    new_connection)

        # set the connection
        player.connection = old_connection
        if old_connection:
            self.connections[old_connection] = player


# if server get's a new connection

# server;bob;login
# server;bob;create,world1
# world1;bob;(1, 0)
# server;tim;login
# server;tim;join,world1
# world1;tim;(1, 1)
# world1;tim;undo
# server;kevin;login
# server;kevin;watch,world1

# the boundary will be what dictates how the transactions are created
# if the boundary is associated with the server...
# if the boundary is an unauthenticated blob...
# if the boundary is bob...

#   def main_loop():
#       accept input (which could be):
#           new connections to the server socket (new players)
#           players connecting to or creating new games
#           players placing pieces
#           players undoing moves
#           players/observers watching the game (can move back an forth)
#           players/observers leaving/quiting games
#
#       handle the input
#

