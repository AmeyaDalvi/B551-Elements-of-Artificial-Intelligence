# Assignment 2

## Team members: Ameya Dalvi, Henish Shah, Shubham Bhagat

# Part 1: Raichu
## State Abstraction:
### Set of Valid States: 
All possible permutation of boards which contains pichu, pikachu and raichu of both players – white as well as black.

### Initial state:
Initial state will be a valid board which contains pichu, pikachu and raichu of both players – white as well as black and passed as command line argument

### Successor function:
Takes a board as input and returns a set of valid boards where either for Player – white or black:

#### 1] A Pichu:
- one square forward diagonally, if that square is empty. 
- jumps over a single Pichu of the opposite color by moving two squares forward diagonally if that square is empty. The jumped piece of opponent team is removed from the board as soon as it is jumped. 

#### 2] A Pikachu:
- Moves 1 or 2 squares either forward, left, or right (but not diagonally) to an empty square, as long as all squares in between are also empty.
- jumps over a single Pichu/Pikachu of the opposite color by moving 2 or 3 squares forward, left, or right (not diagonally), as long as all of the squares between the Pikachu’s start position and jumped piece are empty and all the squares between the jumped piece and the ending position are empty. The jumped piece of opponent player is removed as soon as it is jumped. 

#### 3] A Raichu: created when a Pichu or Pikachu reaches the opposite side of the board 
- Moves any number of squares forward/backward, left, right or diagonally, to an empty square, as long as all squares in between are also empty. 
- Jumps over a single Pichu/Pikachu/Raichu of the opposite color and landing any number of squares forward/backward, left, right or diagonally, as long as all of the squares between the Raichu’s start position and jumped piece are empty and all the squares between the jumped piece and the ending position are empty. The jumped piece of opponent player is removed as soon as it is jumped. 

Successor function considers that 
*Pichus can only capture Pichus, Pikachus can capture Pichus or Pikachus, while Raichus can capture any piece of opponent player**




### Heuristic Function

We have used 3 heuristics for computing the optimal (best) successor for any given board.

#### 1] Heuristic 1:
- This computes the aggregate of the weighted difference in the number pichus, pikachus and raichus respectively for both players.
- For any given player, maximizing this heuristic would increase their chances of winning.

#### 2] Heuristic 2:
- This computes the value which is inversely related to the distance for any piece (pichu or pikachu) to reach the opposite side. The lesser the distance, the greater is this value which increases the likelihood of selecting a successor. 

#### 3] Heuristic 3:
This computes the number of boxes(positions) that a given piece can control from its position. This indicates the number of moves that piece can make. 


### Goal State:
A board where one player captures all the pieces of opponent player


### Approach:

- For our program, we have used minimax algorithm with alpha-beta pruning up to height = 2
- So, for any given board, we will take 2 levels of successors into consideration. Here, the max-player will select the maximum value from beta values returned by its successors, and the min-player will select the minimum value from alpha values returned by its successor.
- Likewise, each player at any given state will try to maximize its chances of winning.

*The output that we are getting takes an average time of 5~6 secs for height 2. We also tried running the algorithm for height 3 and height 4, which gave better results but took a longer time of ~9.76secs and ~80secs respectively.*

![Screen Shot 2021-11-05 at 10 44 58 PM](https://media.github.iu.edu/user/18454/files/81c61600-3e93-11ec-80cf-ae5fdf4cc061)








# Part 2: The Game of Quintris

## State Abstraction:
### Initial state:
The initial state would be the empty board which is initiated at the start of the game.

### Successor function:
The successor function calculates the set of all the possible states where a piece and all its subsequent transformations could be placed in the map.

### Heuristic:
comp_lines : This takes into account, the number of lines completed. This heuristic which we would be maximising, would have the maximum weight in our algorithm.
line_fill : This takes into account the extent to which a particular line is filled in the map. The score increases quadratically as a particular row is filled. We would try to maximize this heuristic. 
agg_height : This takes into account the height of each column of the map. We would be minimising this heuristic
holes : This calculates the total number of holes in the entire map. We would try to minimise this heuristic.
bumpiness : This calculates the unevenness of the entire map. We would try to minimise this heuristic.  

### Goal state:
There is no particular goal state for this algorithm. Ideally, it would aim to run the code forever and keep on increasing the score.

### Algorithm:
The algorithm used in this instance is Expectimax with depth two. 

## Implementation:
For this algorithm, we make use of the SimpleQuintris() interface for our game to run. For a given board and piece, our algorithm calculates all the successor states for that piece and its transformation. Post that, it looks into the next piece and calculates all the possible successor states thereon. Thus, for each piece, it gives the best possible successor from a tree of depth two.
For returning the string of moves, we found that a piece would not transform if it reaches the far-right side of the map. Thus, for the cases where our pieces have to move to the right, the algorithm would first transform the piece and then shift it. 
The average score that our algorithm achieves is in the range of ~60.


## Terminal Output:
<img width="1440" alt="Screen Shot 2021-11-05 at 10 15 22 PM" src="https://media.github.iu.edu/user/18308/files/01071a00-3e93-11ec-9234-320fe87bf04a">

<img width="1440" alt="Screen Shot 2021-11-05 at 10 06 05 PM" src="https://media.github.iu.edu/user/18308/files/082e2800-3e93-11ec-87cf-73f867ee2bdd">





# Part 3: Truth be Told
## Implementation:
- For the classifier, we have made use of CountVectorizer class of the SkLearn module in python.
- CountVectorizer converts a collection of text documents to a matrix of token counts.
- This implementation produces a sparse representation of the counts using scipy.sparse.csr_matrix.
- If you do not provide an a-priori dictionary and you do not use an analyzer that does some kind of feature selection then the number of features will be equal to   the vocabulary size found by analyzing the data.
- The dDict and tDict contain the count of a set of all the words present under the deceptive and truthful label respectively. 
- prob_of_D and prob_of_T store the initial prior probabilities P(D) and P(T) respectively (which is equal to 0.5 initially).
- We ignore all the verbage in all the given sentences by removing words that contain numerals, exclamations, etc. We have used regex for this.
- Doing this itself helped us a lot in improving our accuracy by almost 3%.
- The count_line_D and count_line_D dictionaries store a key-value pair where the key is a unique word and value is the count of that word in a line of dList and     tList respectively.
- prob_of_word_D and prob_of_word_T is the probability of a particular word in either dList or tList. This dictionary stores the probability of a word P(W) for all   words in the dList and tList. 
- Now, we apply the Bayes law to compute the probability of a line in the test data set either being Deceptive or Truthful.
- When we floor divide an element with 5 we get the ideal row location for that element.
- Based on our Bayes Law probabilities, we classify lines of the dataset as either deceptive or truthful.
- Currently, we were able to achieve an accuracy of 83% (332/400 lines classified correctly.

## Terminal Output:
<img width="755" alt="Screen Shot 2021-11-05 at 11 32 52 PM" src="https://media.github.iu.edu/user/18308/files/1891d300-3e92-11ec-8b2a-7bb5f9a57709">


## Silo Output:
<img width="755" alt="Screen Shot 2021-11-05 at 11 35 42 PM" src="https://media.github.iu.edu/user/18308/files/1f204a80-3e92-11ec-935b-fc57efab01eb">


