
import logging
import logging.config
import re
import yaml

from entities.entity import get_character

logger = logging.getLogger("entity_attack")

def attack_event_test(actor, command):

    match = re.match("attack (\w+)", command)

    if match:
        event = {
                    "actor" : actor,
                    "victim" : match.groups()[0],
                    "handler" : attack_event_handler,
                }
    else:
        event = None

    return event


def attack_event_handler(event):

    attacker = get_character(event.get("actor"))
    victim = get_character(event.get("victim"))

    logger.error(f"{event.get('actor')} is attacking {event.get('victim')}!")


if __name__ == "__main__":

    with open("logging_config.yml", "r") as stream:
        config = yaml.load(stream)

    logging.config.dictConfig(config)
    
    event = attack_event_test("bob", "attack tom")
    if event:
        event["handler"](event)

