#!/usr/bin/python3.4

import random

"""
2d6+3
Roll two die 1-6 then add 3.
"""
def roll(num_die, sides, modifier):
    total = 0
    for i in range(num_die):
        total = total+random.randint(1,sides)
    total = total+modifier
    return total

if __name__ == "__main__":

    """
    for i in range(20):
        print(random.randint(1,6))

    md = {}
    md[1] = 0
    md[2] = 0
    md[3] = 0
    md[4] = 0
    md[5] = 0
    md[6] = 0
    for i in range(10000):
        num = random.randint(1,6)
        md[num] = md[num] + 1

    print(md)
    """

    print(roll(1,6,0))
    print(roll(1,8,7))