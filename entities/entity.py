

import random

class Entity(object):

    def __init__(self, name, hp=10, max_hp=10, ab_str=10):

        self.name = name
        self._hp = hp
        self._max_hp = max_hp
        self._ab_str = ab_str

    @property
    def hp(self):
        return self._hp

    @property
    def max_hp(self):
        return self._max_hp

    @property
    def ab_str(self):
        return self._ab_str

    def __repr__(self):
        return f"<{self.name} {self.hp}/{self.max_hp}>"


def get_str_mod(character):
    return (character.ab_str - 10)/2


def get_dmg(event):

    character = get_character(event.name)
    str_mod = get_str_mod(character)

    dmg = random.choice(range(1, 7))
    return int(dmg + str_mod)


def update_character(entity):
    characters[entity.name] = entity


def get_character(name):
    return characters.get(name)


def change_hp(e, amount):
    return Entity(e.name, e.hp + amount, e.max_hp)


characters = {
    "bob" : Entity("bob", hp=11, max_hp=11),
    "tom" : Entity("tom", hp=10, max_hp=10),
    "jim" : Entity("jim", hp=7, max_hp=13),
}


if __name__ == "__main__":

    print(characters)
    
