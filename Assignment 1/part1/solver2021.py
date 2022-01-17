#!/usr/local/bin/python3
#
# Solver 2021
#
# Submitted by : Ameya Dalvi , abdalvi
#
# Based on skeleton code provided in CSCI B551, Fall 2021.


import sys
import copy

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

#---------Logic to find row transformation-------------------
# Referred from https://stackoverflow.com/questions/2150108/efficient-way-to-rotate-a-list-in-python

def shiftrowL(x,row):
    y=x[row-1]
    x[row-1] = y[1:]+y[:1]
    return x

def shiftrowR(x,row):
    y=x[row-1]
    x[row-1] = y[-1:]+y[:-1]
    return x

#---------Logic to find column transformation-----------------
def colshiftU(x,col):
    temp = x[0][col-1]
    for i in range(len(x)):
        if i+1>= len(x):
            break
        x[i][col-1]= x[i+1][col-1]
    x[4][col-1]=temp
    return x

def colshiftD(x,col):
    temp = x[4][col-1]
    for i in range(len(x),0,-1):
        if i-1< 1:
            break
        x[i-1][col-1]= x[i-2][col-1]
    x[0][col-1]=temp
    return x

#---------Logic to find clockwise transformation for inner and outer loops----------
# Refered from: https://www.geeksforgeeks.org/rotate-matrix-elements/
def clock(x,loop):
 
    if not len(x):
        return

    if loop == 'O':
        top = 0
        bottom = len(x)-1

        left = 0
        right = len(x[0])-1

    if loop == 'I':
        top = 1
        bottom = len(x)-2

        left = 1
        right = len(x[0])-2        
    
    prev = x[top+1][left]
    for i in range(left, right+1):
        curr = x[top][i]
        x[top][i] = prev
        prev = curr

    top += 1

    for i in range(top, bottom+1):
        curr = x[i][right]
        x[i][right] = prev
        prev = curr

    right -= 1

    for i in range(right, left-1, -1):
        curr = x[bottom][i]
        x[bottom][i] = prev
        prev = curr

    bottom -= 1

    for i in range(bottom, top-1, -1):
        curr = x[i][left]
        x[i][left] = prev
        prev = curr

    left += 1
    return x

#---------Logic to find anticlockwise transformation for inner and outer loops----------
def aclock(x,loop):
 
    if not len(x):
        return

    if loop == 'O':
        top = 0
        bottom = len(x)-1

        left = 0
        right = len(x[0])-1

    if loop == 'I':
        top = 1
        bottom = len(x)-2

        left = 1
        right = len(x[0])-2        
    
    prev = x[top][left+1]
    for i in range(top, bottom+1):
        curr = x[i][left]
        x[i][left] = prev
        prev = curr

    left += 1

    for i in range(left, right+1):
        curr = x[bottom][i]
        x[bottom][i] = prev
        prev = curr

    bottom -= 1

    for i in range(bottom, top-1, -1):
        curr = x[i][right]
        x[i][right] = prev
        prev = curr

    right -= 1

    for i in range(right, left-1, -1):
        curr = x[top][i]
        x[top][i] = prev
        prev = curr

    top += 1

    return x

# From each state there would always be 24 possible successors 
# 1. With all rows shifted one by one to Left and right ( 10 transformation )
# 2. With all column shifted one by one Up and Down ( 10 transformation )
# 3. Outer ring Clock and AntiClockwise ( 2 transformations )
# 4. Inner ring CLocl and AntiClockwise ( 2 transformations )
def successors(state):
    succ = []
    succ.append((shiftrowL(copy.deepcopy(state),1),"L1"))
    succ.append((shiftrowL(copy.deepcopy(state),2),"L2"))
    succ.append((shiftrowL(copy.deepcopy(state),3),"L3"))
    succ.append((shiftrowL(copy.deepcopy(state),4),"L4"))
    succ.append((shiftrowL(copy.deepcopy(state),5),"L5"))
    succ.append((shiftrowR(copy.deepcopy(state),1),"R1"))
    succ.append((shiftrowR(copy.deepcopy(state),2),"R2"))
    succ.append((shiftrowR(copy.deepcopy(state),3),"R3"))
    succ.append((shiftrowR(copy.deepcopy(state),4),"R4"))
    succ.append((shiftrowR(copy.deepcopy(state),5),"R5"))
    succ.append((colshiftD(copy.deepcopy(state),1),"D1"))
    succ.append((colshiftD(copy.deepcopy(state),2),"D2"))
    succ.append((colshiftD(copy.deepcopy(state),3),"D3"))
    succ.append((colshiftD(copy.deepcopy(state),4),"D4"))
    succ.append((colshiftD(copy.deepcopy(state),5),"D5"))
    succ.append((colshiftU(copy.deepcopy(state),1),"U1"))
    succ.append((colshiftU(copy.deepcopy(state),2),"U2"))
    succ.append((colshiftU(copy.deepcopy(state),3),"U3"))
    succ.append((colshiftU(copy.deepcopy(state),4),"U4"))
    succ.append((colshiftU(copy.deepcopy(state),5),"U5"))
    succ.append((aclock(copy.deepcopy(state),"O"),"Occ"))
    succ.append((aclock(copy.deepcopy(state),"I"),"Icc"))
    succ.append((clock(copy.deepcopy(state),"O"),"Oc"))
    succ.append((clock(copy.deepcopy(state),"I"),"Ic"))

    return succ

# The heuristic function is a modified manhattan distance.
# In each case we check the values for the x and y coordinates of the manhattan distance.
# As the game works like a circularly linked list where each row and column is connected circularly to itself,
# every time when the cost of one of the absoluted coordinates is 4 we, change it to 1.
# Similarly, when the cost of one of the absoluted coordinates is 3 we, change it to 2.
# And only now we add the x and y coordinates to get the correct admissible manhattan distance.
# We can get the ideal row and column coordinates of an element.
# When we floor divide an element with 5 we get the ideal row location for that element.
# When we modulo divide an element with 5 we get the ideal column location for that element.
# In the end, as when we perform any row, column or ring transformation, we move atleast 5 elements at a time.
# So here, we divide the cumulative manhattan distance by 5 befor returning.
def heuristic(succ1):
   
    manhatt=0
  
    for i in range(len(succ1)):
        for j in range(len(succ1[i])):
            currX = i
            currY = j
            current = succ1[i][j]
            goalrow = (current-1)//5  # gives the row coordinate where the element should ideally be
            goalcolumn = (current-1)%5   # gives the column coordinate where the element should ideally be
            zero0 = abs(goalrow-currX)
            one1 = abs(goalcolumn-currY)
            if zero0 == 4:
                zero0= 1
            if zero0 == 3:
                zero0=2
            if one1 == 4:
                one1 = 1
            if one1 == 3:
                one1 = 2
            manhatt += zero0 + one1
    # print(manhatt)
    return manhatt//5

# used this function to sort the fringe based on heuristic
def sortFringe(fringe):
    fringe.sort(key = lambda x: x[1])
    return fringe

# check if we've reached the goal
def is_goal(state,goal):
    if state == goal:
        return True
    return False

# convert initial state received in tuple to list
def to_matrix(state, n):
    return [state[i:i+n] for i in range(0, len(state), n)]

# convert a state from list to tuple
def stateToTuple(state):
    newState = []
    for i in state:
        newState.append(tuple(i))
    return tuple(newState)

# implemented backtracking to get the path 
def getPath(prev,start,goal):
    current=stateToTuple(goal)
    start = stateToTuple(start)
    finalPath=[]
    while True:  
        finalPath.insert(0,prev[current][1])
        if prev[current][0] == start:
            break
        current = prev[current][0]

    return finalPath

# Solver function where we implement the A* Search algoithm
def solve(state):
    state = to_matrix(list(state),5)
    start_state = (copy.deepcopy(state))
    visited=[state]
    succ = []
    goal = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]
    prev={}
    fringe=[]
    
    fringe = [((state,0),heuristic(state) + 0)]

    while fringe:
        
        fringe = sortFringe(fringe)
        (curr_state,curr_dist) = fringe.pop(0)[0]

        for succ in successors(curr_state):
            if is_goal(succ[0],goal):
                prev[stateToTuple(succ[0])]=(stateToTuple(curr_state),succ[1])
                return getPath(prev,start_state,goal)
                            
            elif succ[0] not in visited:
                fringe.append(((succ[0], curr_dist+1), heuristic(succ[0]) + curr_dist+1))

                visited.append(succ[0])
                prev[stateToTuple(succ[0])]=(stateToTuple(curr_state),succ[1])
        

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]
    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))
    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))






