
humanoid_eq = ["right_hand", "left_hand", "right_ring", "left_ring",
                "armor", "head", "neck"]

class Equipment(object):

    def __init__(self, slots=humanoid_eq):
        self.slot_names = slots
        for slot in slots:
            object.__setattr__(self, slot, None)

