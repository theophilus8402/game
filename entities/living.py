
from . import Entity
from .equipment import Equipment

class Living(Entity):

    def __init__(self, name, id=None):
        super().__init__(name, id)
        self.eq = Equipment()

    def __repr__(self):
        return "<{}: {}, living>".format(self.id, self.name)

    def equip(self, item, slot, both_hands=False):
        if both_hands:
            self.eq.right_hand = item
            self.eq.left_hand = item
        elif slot in self.eq.slot_names:
            self.eq.__setattr__(slot, item)
        else:
            raise KeyError("{} is not a valid equipment slot.".format(slot))


