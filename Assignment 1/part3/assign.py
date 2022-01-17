#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: SHUBHAM NARENDRA BHAGAT , snbhagat
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

from itertools import combinations
import sys
import time
import copy


# The successor take input as list of teams and list of pending students. It will create combinations from list of pending students.
# The combination-list will be a list of list of teams - where each list of team will have 1, 2 or 3 teams.
# After getting all possible combinations of students still not assigned, we append that list of team to the successor popped.

# Example: from list of students say - [A, B, C, D, E] and [[A,B,C]] is the successor popped,
# sucessor function will generate successors (list of teams) such as -
# [[ABC],[C]] , [[ABC],[D]], ........[[ABC],[C,D]]..........[[ABC],[C,D,E]]

def sucessors(current_list, pendingList):
    succ_list= []
    combList = []
   
    
    #append single student grouplist
    list_of_1 = combinations(pendingList,1)
    for tup in list_of_1:
        combList.append(tup)

    #append group of 2 to the grouplist
    list_of_2 = combinations(pendingList,2)
    for tup in list_of_2:
        combList.append(tup)

    #append group of 3 to the grouplist
    list_of_3 = combinations(pendingList,3)
    for tup in list_of_3:
        combList.append(tup)
    
    
    #create successor list for current successor
    for comb in combList:
        succ = copy.deepcopy(current_list)
        succ.append(comb)
        succ_list.append(succ)
    return succ_list



# This function will sort the fringe according to the total cost of each successor.
# used for A* algorithm
def sortFringe(fringe):
        fringe.sort(key = lambda x: x[1])
        return fringe


# This function will take input as a successor and check whether it is goal or not. 
# i.e: It will check if all the current successor has all the students present in it.
def foundGoal(succ,studentList):
    count = 0
    for group in succ:
        for student in group:
            if student in studentList:
                count +=1
    if count == len(studentList):
        return True
    else:
        return False


# This us the cost function which will calculate the total time it will take to grade each successor
# for any list of teams it takes into consideration 4 cases:
#       - It will take 5 minutes to grade each assignment, so total grading time is 5 times the number of teams.
#       - Each student who requested a specific group size and was assigned to a different group size will send
#         a complaint email to an instructor, and it will take the instructor 2 minutes to read this email.
#       - If a student is not assigned to someone they requested, there is a 5% probability that the two students
#         will still share code, and if this happens it will take 60 minutes for the instructor to walk through the
#         Academic Integrity. So the time will be 0.05 * 60 = 3 mins
#       - Each student who is assigned to someone they requested not to work with (in question 3 above)
#         complains to the Dean, who meets with the instructor for 10 minutes
def findTime(groupList, group_pref):
    total_time = 5 * len(groupList)

    for group in groupList: 
        for student in group:
            number_of_partners = group_pref[student]['num_of_partners']
            if((number_of_partners != len(group)) and (number_of_partners != 0) ):
                total_time += 2
            for person in group_pref[student]['include']:
                if (person == 'xxx' or person == 'zzz' ):
                    break
                if person not in group:
                    total_time += 3
            for person in group_pref[student]['exclude']:
                if person == "_":
                    break
                if person in group:
                    total_time += 10
    return total_time

# This function will take a successor as input and give output as list of students which are not in current successor.
def getPendingList(current_list, studentList):
    pendingList = []
    studentList = set(studentList)
    temp = set()
    if len(current_list) == 0: #handle initial condition where currentList is empty
        pendingList = studentList
    else:
        for group in current_list:
            for student in group:
                if student in studentList:
                    temp.add(student)
        pendingList = list(studentList - temp)
    return pendingList


# create the goal dictionary to yeild
def getGoalDict(succ, total_time):
    finalGroupList = []
    for tup in succ:
        team = '-'.join(tup)
        finalGroupList.append(team)
    return {"assigned-groups": finalGroupList, "total-cost" : total_time}





def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """

    file = open(input_file, "r")
    studentList = []
    group_pref = {}
    num_of_partners = 0
    partners = ""
    for line in file:    
        word_list = line.split()
        key = word_list[0]
        studentList.append(word_list[0])
        partners = word_list[1].split('-')
        num_of_partners = len(partners)
        group_pref[key] = {}
        group_pref[key]['num_of_partners'] = num_of_partners
        group_pref[key]['include'] = partners
        group_pref[key]['exclude'] = word_list[2].split(',')
    file.close()

    fringe =[ [[],0]  ]
    min_time = 10000

# Currently, we have implemented DFS algorithm to get a quick solution. Once we get first solution we yeild that and algorithm continues.
# Afterwards, if we get a new solution we check whether the new solution takes less time that previous solution or not. If yes, we yeild that solution otherwise continue.
# In this way, each subsequent solution will have lesser grading time than previous solution. Thus, in each iteration, we get a more optimal solution than previous one.

# ======================================= IMPORTANT POINT ========================================================
# Note: while executing pytest, for test2.txt sometimes the algorithm takes more time than predefined threshold. Thus, is may not pass the test2 for one particular execution.
# Since we have implemented DFS, sometimes the first successor popped has time - 80 or even 101 and may take long time to reach the lowest possible value (43) within the 
# specified time. However, if time is not constratint , the algorithm will ALWAYS reach lowest time- 43.

# In my report I have excluded screenshot for two execution instances of the program on silo, one which fails testcase 2 and another which passes all testcases.
# I have also included output screenshots for proof.
# ================================================================================================================
    while fringe:
        #fringe = sortFringe(fringe)  # For A* algorithm, uncomment this line and due fringe.pop(0). For BFS just do fringe.pop(0)
        
        (current_list, current_time) = fringe.pop() #dfs  
        pendingList = getPendingList(current_list,studentList)
        for succ in sucessors(current_list, pendingList):
            total_time = findTime(succ, group_pref)
            if foundGoal(succ,studentList) and total_time < min_time:
                yield(getGoalDict(succ, total_time))
                min_time = total_time
            else:
                fringe.append([succ,total_time])

    
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
   
    
