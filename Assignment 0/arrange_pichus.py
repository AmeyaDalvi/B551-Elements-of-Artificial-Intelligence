#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Ameya Dalvi, abdalvi
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys
import pdb

global pichus 

pichus=[(5,0)]

# pichus=[[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]]

# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# # Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
# def add_pichu(house_map, row, col):
#     return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# The attac function is implemented in such a way that it should iteratively check if when a pichu gets placed on the map, 
# if it isn’t under attack by any other pichu or not. 
# If there’s an obstruction “X” in between any two pichus and there isn’t any attack on it by all the other pichus, 
# its safe to place that pichu at that position on the board.

def attac(row,col,pichuslist,x_list):
    for pos in pichuslist:
        for x in x_list:
            # print("row:",row)
            # print("col:",col)
            # print("pos",pos)
            if col == pos[1] == x[1] or row == pos[0] == x[0]:
                # if((row,col)< x < pos) or (pos < x < (row,col)):
                #     return False
                if((row< x[0]< pos[0]) or (col< x[1] < pos[1])) or ((pos[0] < x[0] < row) or (pos[1] < x[1] < col)):
                    return False
            # elif col == pos[1] != x[1] or row == pos[0] != x[0]:
            #     return True
            
    return True   

            # if ((col != pos[1] and row != pos[0])):
            #     if(row,col)< x < pos or pos < x < (row,col):
            #         return True                 


# successors are only generated if and only if none of the pichus are under attack by one another
def successors(house_map):
    #x_list=[[(row_i,col_i) for row_i in range(len(house_map)) for col_i in range(len(house_map[row_i])) if house_map[row_i][col_i]=="X"][0]]
    x_list=[]
    for row_i in range(len(house_map)):
        for col_i in range(len(house_map[row_i])):
            if house_map[row_i][col_i]=="X":
                x_list.append((row_i,col_i))

    # print(pichus)
    # print(x_list)
    for r in range(0, len(house_map)):
        for c in range(0, len(house_map[0])):
            if house_map[r][c]== ".":
                if (attac(r,c,pichus,x_list)): 
                    continue
                else:
                    pichus.append((r,c))
                    return [ add_pichu(house_map, r, c) ] #pichu only appeneded if its safe to place it on the map


# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k 

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#

# Get list of successors of given house_map state

# def successors(house_map):
#     return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.' ]

def solve(initial_house_map,k):
    fringe = [initial_house_map]
    # print(fringe)
    while fringe:
        current = fringe.pop()
        for new_house_map in successors( current ):
            if new_house_map is not None:
                if is_goal(new_house_map,k):
                    return(new_house_map, True)
                fringe.append(new_house_map)

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")