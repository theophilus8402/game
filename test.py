#!/usr/bin/python3

def display_map(center, dimension):
    map_rows = []     # a list of the string for each row
    x, y = center
    print("Center: {}".format(center))
    for j in range(-dimension, dimension+1).__reversed__():
        row = []
        for i in range(-dimension, dimension+1):
            coord = (x+i,y+j)
            print("{}+{}, {}+{} == Coord: {}".format(x,i,y,j,coord))

display_map((3, 0), 3)
