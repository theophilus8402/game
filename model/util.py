import enum
import random
from collections import defaultdict, OrderedDict
from math import sqrt

def distance_between_coords(coord1, coord2):
    """Returns the distance between two coords."""
    x1, y1 = coord1
    x2, y2 = coord2
    squared_distance = (x2 - x1)**2 + (y2 - y1)**2
    return sqrt(squared_distance)


"""
2d6+3
Roll two die 1-6 then add 3.
"""
def roll(num_die, sides, modifier=0):
    """
    Generates random number (num_die number of times) from 1 to number of sides
    (inclusive).  Returns the sum of all the generated numbers and the modifier.
    Example: 2d6+3
    """
    total = 0
    for i in range(num_die):
        total = total+random.randint(1,sides)
    total = total+modifier
    return total


class RollInfo():

    def __init__(self, num_die, sides, flat_bonus=0, bonuses=[]):
        self.bonuses = bonuses
        self.flat_bonus = flat_bonus
        self.roll_result = roll(num_die, sides)
        self.calculate_total()

    def calculate_total(self):
        bonus_total = sum([bonus.amount for bonus in self.bonuses])
        self.total = self.flat_bonus + bonus_total + self.roll_result

    def __repr__(self):
        # 20+2-3+1
        if self.flat_bonus > 0:
            roll_str = ["{}+{}".format(self.roll_result, self.flat_bonus)]
        elif self.flat_bonus < 0:
            roll_str = ["{}{}".format(self.roll_result, self.flat_bonus)]
        else:
            roll_str = ["{}".format(self.roll_result)]
        for bonus in self.bonuses:
            if bonus.amount >= 0:
                roll_str.append("+{}".format(bonus.amount))
            else:
                roll_str.append("{}".format(bonus.amount))
        return "{}={}".format("".join(roll_str), self.total)


@enum.unique
class RollType(enum.Enum):
    critical_miss = 0
    miss = 1
    dodge = 2
    block = 3
    hit = 4
    critical_hit = 5


attack_poss_types = [RollType.critical_miss, RollType.miss, RollType.hit,
    RollType.critical_hit]
defence_poss_types = [RollType.dodge, RollType.block]


def new_roll(possibilities):
    """
    Input: An ordered dictionary of roll types (key) and "possibilities" (value).
    Sums the possibilities, generates a random number 0-total.  Based on the "roll",
    the number will dictate which type was rolled/selected.
    Returns (data_type, number_rolled).
    """
    total = sum([poss for poss in possibilities.values()])
    roll = random.randint(1, total)
    possibility_max = 0
    for roll_type, possibility in possibilities.items():
        possibility_max += possibility
        if roll <= possibility_max:
            break
    return roll_type, roll


if __name__ == "__main__":
    poss = OrderedDict()
    poss[RollType.critical_miss] = 5
    poss[RollType.miss] = 10
    poss[RollType.block] = 10
    poss[RollType.dodge] = 10
    poss[RollType.hit] = 40
    poss[RollType.critical_hit] = 5

    results = defaultdict(lambda: 0)
    for i in range(1000):
        roll_type, roll = new_roll(poss)
        results[roll_type] += 1

    for rtype, count in results.items():
        print("{} = {}".format(rtype, count))
