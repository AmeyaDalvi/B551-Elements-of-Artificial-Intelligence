# Assignment 1
## Team members: Ameya Dalvi, Henish Shah, Shubham Bhagat



# Part 2: Road Trip
## Assigned member: Henish Shah

### State Space:
The state space for this problem statement is the exhaustive set of all possible routes from point ‘A’ to point ‘B’ essentially covering all the cities in the map.

### Successor Function:
The successor function for any point returns the set of cities/nodes directly connected to it.

### Edge Weights:
Based on the given input of the cost function i.e. ‘time’, ’segments’, ’distance’ or ‘delivery’ we minimise the respective parameters for our desired route.

### Goal State:
The goal state is nothing but the final end node/ final destination of our route.

### Heuristic Function:
The heuristic function for this problem statement is *Haversine distance*. This is an admissible heuristic function due to the fact that it takes into consideration the longitude and the latitude of the cities. Thus, the distance is essentially a straight line drawn along the surface of the earth between two cities which will always be less than the actual distance of the route between them (the heuristic function never overestimates)

### Search Algorithm:
The search algorithm used for this problem statement is A* search. This technique always returns the optimal solution. As we use a priority queue based on a weighted combination of the heuristic function and the cost function *{a\*h(s) + g(s)}*
 
### Exceptional Cases:
There were some cities for which there were no co-ordinates. The initial approach we took was trying to find the missing co-ordinates (Point C) such that for two of its successor nodes whose co-ordinates are given (Point A, Point B), the three points form a triangle. Forming a triangle, given the sides AB, BC, AC we tried to find the co-ordinate of point C. The reason that it did not work was because we have longitude and latitude instead of cartesian co-ordinates (If given more time and by doing a few adjustments, I’m sure that this approach should work for the longitudes and latitudes as well). 



 

![image](https://media.github.iu.edu/user/18454/files/76300100-288d-11ec-940b-1dcaad3e719a)


Although, we then considered returning the heuristic value as 0 for cases where the co-ordinates are missing. This substitute also works seamlessly for such cases.

### pytest on Silo
![silo output](https://media.github.iu.edu/user/18454/files/62d26500-2890-11ec-84c7-39a0d91e131f)




<br>

# Part 3: Assign Teams
## Assigned member: Shubham Narendra Bhagat

### Set of valid states:
All possible list of teams, where each team is formed from all possible combination for a given list of students.

### Initial state:
List of teams which is empty. i.e.: No teams formed yet.

### Successor function: 
The successor take input as list of teams and list of pending students. It will create combinations from list of pending students. The combination-list will be a list of lists of teams - where each list of teams will have 1, 2 or 3 teams. After getting all possible combinations of students still not assigned, we append that list of teams to the successor popped.

Example: from list of students say - [A, B, C, D, E] and [[A, B, C]] is the successor popped,
Successor function will generate successors (list of teams) such as -
[[ABC], [C]], [[ABC], [D]], ........[[ABC], [C, D]] ..........[[ABC], [C, D, E]]

### Cost function: 
This function will calculate the total time it will take to grade each successor
For any list of teams, it takes into consideration 4 cases:
-	It will take 5 minutes to grade each assignment, so total grading time is 5 times the number of teams.
-	Each student who requested a specific group size and was assigned to a different group size will send
-	a complaint email to an instructor, and it will take the instructor 2 minutes to read this email.
-	If a student is not assigned to someone they requested, there is a 5% probability that the two students will still share code, and if this happens it will take 60 minutes for the instructor to walk through the Academic Integrity. So, the time will be 0.05 * 60 = 3 mins
-	Each student who is assigned to someone they requested not to work with, complains to the Dean, who meets with the instructor for 10 minutes
The total cost will be cumulative of time is takes for all above cases.

### Goal state: 
A list of teams which contains all the students.

## Approach:

-	Currently, we have implemented DFS algorithm to get a quick solution. Once we get first solution, we yield that, and algorithm continues to find another solution.
-	Afterwards, if we get a new solution, we check whether the new solution takes less time that previous solution or not. If yes, we yield that solution otherwise continue.
-	In this way, each subsequent solution will have lesser grading time than previous solution. 
-	Thus, in each iteration, we get a more optimal solution than previous one.

### Pseudocode:
```
min_time = 1000
fringe = [ [(),0] ] #Empty list of teams
while fringe:
	current  fringe.pop ()
	successor _list  successor (current, pending_student_list)
	for each succ in successor_list:
		calculate total time
		if succ == goal and total_time < min_time
			yeild solution
			min_time = total_time
		else:
			fringe.append(succ)
```
### IMPORTANT NOTE:

While executing pytest, for test2.txt sometimes the algorithm takes more time than predefined threshold. Thus, it may not pass the test2 for one execution but not for every instance of execution.
Since we have implemented DFS, sometimes the first successor popped has time - 80 or even 101 and may take long time to reach the lowest possible value (43) within the 
specified time. However, if time is not constraint, the algorithm will ALWAYS reach lowest time- 43.


 ### Output on terminal - test1.txt

  <img src="https://media.github.iu.edu/user/18454/files/bc369600-2888-11ec-8680-f3255c067467" width="350" title="test1 output">


### Output on terminal - test2.txt

  <img src="https://media.github.iu.edu/user/18454/files/98c01b00-2889-11ec-8af6-8473d47ff096" width="350" title="test2 output">


### Output on terminal - test3.txt

  <img src="https://media.github.iu.edu/user/18454/files/2d2a7d80-288a-11ec-8656-e022ec2efc81"  title="test3 output">


### Pytest on Silo

As I mentioned above for one instance of pytest, the test failed but on subsequent instance of pytest, the test passed. This ambiguity happens due to unpredictable nature (incompleteness) of DFS

![silo](https://media.github.iu.edu/user/18454/files/c73ef580-288b-11ec-96e6-92f35ad7f3e7)

### Pytest on local memory

<img width="1154" alt="pytest local" src="https://media.github.iu.edu/user/18454/files/446a6a80-288c-11ec-9c92-30cd42ee92c9">
