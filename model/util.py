from math import sqrt
import random

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


