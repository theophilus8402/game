

class Entity(object):

    def __init__(self, name, hp=10, max_hp=10):

        self.name = name
        self._hp = hp
        self._max_hp = max_hp

    @property
    def hp(self):
        return self._hp

    @property
    def max_hp(self):
        return self._max_hp

----------------------------------------------------------------

def change_hp(e, amount):
    return Entity(e.name, e.hp + amount, e.max_hp)

def handle(event):
    update_character(change_hp(get_character(event.name), event.value))

def main_loop():
    bob = Entity("bob", hp=11, max_hp=11)
    events = event_generator()
    for event in events:
        handle(event) 

----------------------------------------------------------------

if __name__ == "__main__":
    main_loop()

    
