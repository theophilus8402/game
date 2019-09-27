
class World(object):

    def __init__(self, name):
        self.name = name


main_world = World("the_world")

def get_world():
    return main_world

