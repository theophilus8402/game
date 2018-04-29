
from unique_dict import PlayerDict,WorldDict,ConnectionDict
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


class PlayerAlreadyInWorld(Exception):
    pass

class WorldFull(Exception):
    pass


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


class Interactor():

    def __init__(self):

        # self.worlds = {name : World}
        self.worlds = WorldDict()

        # self.players = {name : Player}
        self.players = PlayerDict()

        # self.connections = {connection : Player}
        self.connections = ConnectionDict()

        self.transaction_actions = {
            "create_world" : (self.create_world, self.undo_create_world),
            "create_player" : (self.create_player, self.undo_create_player),
            "join_world" : (self.join_world, self.undo_join_world),
            "change_connection" : (
                   self.change_connection, self.undo_change_connection),
        }

    def apply_transaction(self, trans, undo=False):

        entity_name = trans["entity"]
        action_name = trans["action"]
        action_input = trans["input"]

        if entity_name == "server":
            # the server needs to do something
            entity = self
        else:
            # one of the worlds needs to do something
            entity = self.worlds[entity_name]

        action,undo_action = entity.transaction_actions[action_name]

        if not undo:
            action(**action_input)
        else:
            undo_action(**action_input)

    def create_world(self, game_id):

        # creates the world with the associated name and enters it into
        #   self.worlds

        new_world = World(game_id=game_id)
        self.worlds[game_id] = new_world
        
    def undo_create_world(self, game_id):

        # undoes the creation of the specified world
        # raises a WorldDoesNotExist error if game_id doesn't exist

        del(self.worlds[game_id])

    def create_player(self, name):

        lower_name = name.lower()
        self.players[lower_name] = Player(name)

    def undo_create_player(self, name):

        del(self.players[name.lower()])

    def change_connection(self, name, old_connection, new_connection):

        # find the player
        player = self.players[name.lower()]

        # change the self.connections entries as appropriate
        if old_connection is not None:
            del(self.connections[old_connection])

        # set the connection
        player.connection = new_connection
        if new_connection:
            self.connections[new_connection] = player

    def undo_change_connection(self, name, old_connection, new_connection):

        # find the player
        player = self.players[name.lower()]

        # change the self.connections entries as appropriate
        if new_connection is not None:
            del(self.connections[new_connection])

        # set the connection
        player.connection = old_connection
        if old_connection:
            self.connections[old_connection] = player

    # server;tim;join,world1
    def join_world(self, player_name, game_id):

        # find the player
        player = self.players[player_name.lower()]

        # make sure the player isn't already in a world
        if player.world != None:
            raise PlayerAlreadyInWorld()

        # find the world
        world = self.worlds[game_id]

        # the order in which players join the world will dictate
        # the piece the player gets.  The players can't choose which
        # piece they get to play.  The first player that joins will
        # become the "o" player.  The second will become the "x" player.
        if not world.o_player:

            # add the player to the world
            world.o_player = player.name

            # set the player piece
            player.piece = "o"

        elif not world.x_player:

            # add the player to the world
            world.x_player = player.name

            # set the player piece
            player.piece = "x"

        else:

            raise WorldFull()

        # add the world to the player
        player.world = world.game_id

    def undo_join_world(self, player_name, game_id):

        # find the player
        player = self.players[player_name.lower()]

        # find the world
        world = self.worlds[game_id]

        # remove the player from the world
        if player.piece == "o":
            world.o_player = None

        elif player.piece == "x":
            world.x_player = None

        # remove the player piece
        player.piece = None

        # remove the world from the player
        player.world = None

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

