
from events import event_generator, handle_event

characters = {
    "jerry" : Entity("jerry", hp=11, max_hp=11),
    "tom" : Entity("tom", hp=10, max_hp=10),
    "jim" : Entity("jim", hp=7, max_hp=13),
}

def update_character(entity):
    characters[entity.name] = entity

def get_character(name):
    return characters.get(name)

def change_hp(e, amount):
    return Entity(e.name, e.hp + amount, e.max_hp)

def handle(event):
    update_character(change_hp(get_character(event.name), event.value))


def main_loop():
    events = event_generator()
    for event in events:
        handle_event(event) 

#----------------------------------------------------------------

if __name__ == "__main__":
    main_loop()

    
