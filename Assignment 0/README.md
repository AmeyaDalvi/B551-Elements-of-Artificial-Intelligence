# a0
# Problem 1: Navigation

State Abstraction:

Set of valid states:  
1.	All the states in the housemap where pichu can be placed 
      e.g All “.” Nodes.

Successor function: 
1.	Successor function takes input the current housemap and gives successors where pichu can move by one block (“moves” method in the code)

Cost function: 
1.	Cost function is the sum of the actual path of moving from one node to another which is unit distance =1 and the admissible heuristic used which is the Manhattan Distance in this case. 
2.	Hence, In this case, cost function can be defined as f(s) = g(s) + h(s), where, h(s) is the admissible Heuristic  which is the cost of reaching goal state from current state and g(s) is the cost of reaching current state from initial state.

Goal state definition: 
1.	Goal state is basically Pichu reaching the “@” position, taking the shortest path possible.

Initial state: 
1.	Initial state is the initial house map that’s given in the question.

Issue with the Skeleton code:
The initial skeleton code given was going into an infinite loop. The issue with the code was that we did not keep any track of the previously visited states either by using a separate data structure to store them or store the path from the start node to the goal as we implement the algo hence making it go into an infinite loop as it used DFS by default.

Now to fix this issue, 
1.	I have implemented A* Search that expands those nodes with the minimum value of the cost function f(S) that we have used.
2.	Used a list to store all the visited nodes so that the algo doesn’t keep searching through all the nodes again and again for all the iterations.
3.	A* needs a Priority queue so that the elements that we pop in the fringe are popped based on the lowest cost function.
4.	Hence , I’ve implemented the priority queue using python’s built in module heapq.
5.	I tried implementing the priority queue using dictionaries but faced some issues with it and hence resorted to using a built in module for the same.
6.	To trace the path from start node to the goal, I made use of backtracking; Basically, using the goal node to reach it’s parent node, and tracing in the same manner till we reach our start node and then printing the path.


# Problem 2: Hide and Seek

State Abstraction:

Set of valid states:  
1.	All positions (“. ”) in the house map where “k” pichus can be placed such that no pichus are able to see each other. 

Successor function: 
1.	In my case, successor function takes input the house map, checks if there is any attack when there are n pichus placed already and we try to insert (n+1)th pichu on the map and returns the new state of the house map such that all the n+1 pichus satisfy the basic conditions such that n+1<=k; k being the total number of pichus.

Cost function: 
1.	Cost function is 1 for every pichu that gets added to the house map.

Goal state definition: 
1.	Goal state is the final state where all pichus are correctly placed such that no pichus see each other.

Initial state: 
1.	Initial state is the initial house map that’s given in the question with 1st pichu already placed.

Issue with the Skeleton code:
The initial skeleton code given, basically traverses the whole map and places pichus in line at the end of the map disregarding all the basic cases mentioned in the pdf.

Now to fix this issue, 
1.	To solve this problem, I have tried implementing the Depth First Search algorithm.
2.	My idea was to allow a pichu to be placed in the house map if and only if it doesn’t fall under attack due to the other pichus.
3.	For this, I modified the existing successor function to allow it to place a pichu if and onlt if there is no attack on it
4.	Now, the attack function was implemented in such a way that it should iteratively check if when a pichu gets placed on the map, if it isn’t under attack by any other pichu or not. 
5.	If there’s an obstruction “X” in between any two pichus and there isn’t any attack on it by all the other pichus, its safe to place that pichu at that position on the board.
6.	Unfortunately, after trying this approach in multiple coding styles and tweaking to check if it satisfies all the conditions or not, it is still not able to find the correct goal state.



