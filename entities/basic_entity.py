

class Entity():

    largest_entity_id = -1

    def __init__(self, name, id=None):

        if id == None:
            # determine the id
            Entity.largest_entity_id += 1
            self.id = Entity.largest_entity_id
        else:
            # update the largest_entity_id if appropriate
            if Entity.largest_entity_id < id:
                Entity.largest_entity_id = id

            self.id = id

        self.name = name

    def __repr__(self):
        return "<{}: {}>".format(self.id, self.name)

