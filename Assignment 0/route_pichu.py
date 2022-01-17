#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Ameya Dalvi , abdalvi
#
# Based on skeleton code provided in CSCI B551, Fall 2021.

import sys
#------implemented priority queue using python package heapq--------
#------Refered from https://docs.python.org/3/library/heapq.html----
import heapq

def finaldist(x1,y1,x2,y2,curr_dist): #used manhattan admissible heuristic and calculated the heuristic function f(s) = h(s)+g(s)
        h=abs(x2-x1)+abs(y2-y1) 
        g=curr_dist
        # print("h:",h)
        # print("g:",g)
        return h + g

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1)) 

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]


# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)



#-----------Tried an approach using dictionary to store the fringe and perform A* but had a hard time implementing priorty queue--------

# def search(house_map):
#         # Find pichu start position
#         pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0] 
#         goal_loc = [(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="@"][0]
#         visited=[]
#         fringe= [(pichu_loc,0)]
#         curr_dist1=0
#         dictfringe=dict()

#         while fringe:
#                 print(fringe)
#                 for i,j in fringe:
#                         dictfringe.setdefault(i, []).append(j)
#                 print("dict:",dictfringe)
#                 curr=(curr_move, curr_dist)=fringe.pop(0)
#                 curr1=list(curr)
#                 print("curr1",curr1)
#                 curr1[1]=finaldist(*curr_move,*goal_loc)
#                 print("curr2",curr1)
#                 #curr_dist = finaldist(*curr_move,*goal_loc,curr_dist)
#                 visited.append(curr_move)
#                 print("succ:",moves(house_map, *curr_move))
#                 for move in moves(house_map, *curr_move):
#                         if house_map[move[0]][move[1]]=="@":
#                                 print(move, curr_dist+1)
#                                 return (7, 'DDDDDDD')  # return a dummy answer
#                         elif move not in visited:
#                                 fringe.append((move, curr1[1] + curr_dist1))
#                                 curr_dist1+=1
#                                 #print(move)

#-----------------------------------------------------------------------------------------------------------------------------------------

# getPath function is used to get the final path using backtracking after reaching the goal node
# https://www.codegrepper.com/code-examples/python/heapq+python+with+tuples possible operations on a heap of tuples

def getPath(parentchild,start,goal):
        current=goal
        final_path=[]
        path=""
        while current!=start:
                for tup in parentchild:
                        if tup[1]==current:
                                final_path.insert(0,current)
                                current=tup[0]
                                if (tup[1][0]>tup[0][0]):
                                        path += "D"
                                elif (tup[1][0]<tup[0][0]):
                                        path += "U"
                                elif (tup[1][1]>tup[0][1]):
                                        path += "R"
                                elif (tup[1][1]<tup[0][1]):
                                        path += "L"
        final_path.insert(0,start)
        return (len(path),path[::-1])

# Made use of the heapq package to implement priority queue to perform A* search
# took fringe as a list of tuples which consist of final distance i.e heuristic f(s) for A*, current distance
# and the state we are currently at
# heapq.heappop() basically pops the element with the highest priority/least value; in this case the priority 
# is decided by the first element of the fringe which is the final distance

def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0] 
        goal_loc = [(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="@"][0]
        visited=[(pichu_loc)]
        fringe=[] 
        fringe.append((finaldist(*pichu_loc,*goal_loc,0),0, pichu_loc))
        parentchild=[]


        while fringe:
                (final_dist, curr_dist, curr_move)=heapq.heappop(fringe)
                for move in moves(house_map, *curr_move):
                        if house_map[move[0]][move[1]]=="@":
                                parentchild.append((curr_move,move))  
                                return getPath(parentchild,pichu_loc,goal_loc)                           
                        elif move not in visited:
                                fringe.append((finaldist(*move,*goal_loc, curr_dist+1), curr_dist+1, move))
                                visited.append(curr_move)
                                parentchild.append((curr_move,move)) 
        return (-1,"")

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")        
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])