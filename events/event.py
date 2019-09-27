
from entities import update_character, change_hp, get_character

class Event(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value


def event_generator():
    events = [Event("bob", 3), Event("tom", -4), Event("jim", -2)]
    for event in events:
        yield event


def handle(event):
    update_character(change_hp(get_character(event.name), event.value))


if __name__ == "__main__":

    events = event_generator()
    for event in events:
        handle(event) 

