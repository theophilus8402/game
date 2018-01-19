
from collections import defaultdict
from datetime import datetime,timedelta

def cities():
    for city in ["Berlin", "Hamburg", "Munich", "Freiburg"]:
        yield city

def squares():
    for number in range(10):
        yield number ** 2

def generator_splitted():
    yield from cities()
    yield from squares()

def permutations(items):
    n = len(items)
    if n == 0:
        yield []
    else:
        for i in range(n):
            for cc in permutations(items[:i]+items[i+1:]):
                yield [items[i]] + cc

def get_most_hated(pains):
    most_hated = None
    most_dmg = -1
    for person, dmg in pains.items():
        if dmg > most_dmg:
            most_hated = person
            most_dmg = dmg
    return most_hated

def simple_ai():

    next_action = None
    next_action_time = datetime.now()
    time_between_actions = timedelta(seconds=3)
    # pains = {"bob": 3, "tim": 5}
    pains = defaultdict(lambda: 0)

    while True:

        world_input = yield next_action

        # handle input from the world
        if world_input:
            person, dmg = world_input
            pains[person] += dmg

        now_time = datetime.now()

        # see if I can act
        if next_action_time <= now_time:
            # I can do something!
            next_action_time = now_time + time_between_actions
            # see if there's someone to beatup
            most_hated_person = get_most_hated(pains)
            if most_hated_person:
                next_action = "hit {}".format(most_hated_person)
            else:
                next_action = "*whistle*"
        elif world_input:
            next_action = "I'm going to get you, {}!".format(person)
        else:
            next_action = None

def running_average():
    total = 0
    length = 0
    avg = 0
    while True:
        new_value = yield avg
        total += new_value
        length += 1
        avg = total / length

ra = running_average()  # initialize the coroutine
next(ra)                # we have to start the coroutine
for value in [7, 13, 17, 231, 12, 8, 3]:
    out_str = "sent: {val:3d}, new average: {avg:6.2f}"
    print(out_str.format(val=value, avg=ra.send(value)))


def trange(start, stop, increment):
    current_time = start
    while True:
        yield current_time
        h, m, s = tuple(map(sum, zip(current_time, increment)))
        if s >= 60:
            m += 60
            s = s % 60
        if m >= 60:
            h += 1
            m = m % 60
        current_time = (h, m, s)
        if ((h > stop[0]) or 
            ((h == stop[0]) and (m > stop[1])) or
            ((h == stop[0]) and (m == stop[1]) and (s > stop[2]))):
            break

for time in trange((10, 10, 10), (13, 50, 15), (0, 15, 12) ):
    print(time)

