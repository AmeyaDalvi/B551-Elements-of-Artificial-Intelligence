# Assignment 3
## Team members: Ameya Dalvi, Henish Shah, Shubham Bhagat
# Part 1: Part-of-Speech Tagging

#### We have three major algorithms namely:
1. Simple (Simple Bayes Network)
2. HMM (Viterbi)
3. Complex (MCMC)

### Working:

#### 1.Simplified:
- For this algorithm, since the only connections are between the hidden variable and its corresponding observed variable, we directly calculate the posterior probabilities for each a tag given a word and take the maximum of those probabilities to predict the appropriate tag

#### 2.HMM (Viterbi):
- For this algorithm, we take into consideration the transition and emission probabilities. The main concept of this algorithm is dynamic programming. Thus, we make two tables to store the probability values and their corresponding tags.
- For the initial word, we just consider the initial probabilities (probabilities that a particular tag appears in the first word of a sentence) and the respective emission probabilities. For the following words, we firstly take into consideration the product of transition probabilities and the probabilities received in the previous column, and find the maximum product. Post that, that maximum product is multiplied with the emission probabilities of the current column and this process is repeated.
- Once our tables are ready, we start backtracking to find the best possible path/seq of the tags for a given sentence.

#### 3.Complex (MCMC)
- In this algorithm, we make use of Gibbs sampling method to generate 500 samples for each possible combination of tags for the words in a sentence. By this method, eventually with all the samples, the algorithm converges (tries to converge) on the best possible sequence of the tags. In addition to the emission and transition probabilities calculated in Viterbi, we also consider new set of emission and transition values in this algorithm.

### Silo Output:
![part1](https://media.github.iu.edu/user/18308/files/91397e80-5494-11ec-9443-bbedda4af977)



# Part 2: Ice Tracking
### Using Bayes Net:
- In this approach, we basically find the pixel with the least value in that column and assume it to be the boundary.
- The drawback of this naive approach is that it plots a boundary that is not continuous.
- Assuming that boundaries, in general, are a bit smoother and continuous in nature, having a model that takes into account these details would help in accurately denoting the boundary. 
- Hence to get a more accurate boundary detection we use HMM (Viterbi) in our 2nd approach.

### Using Viterbi Algorithm:
In this approach, we mainly focus on 3 types of probabilities.

1. **Initial Probability:**
Initial probability is calculated by assigning the reciprocal of the total number of rows for each pixel in the first column.
2. **Emission Probability:**
Emission probability is basically the pixel value divided by the sum of pixel values in that pixel column.
3. **Transition Probability:**
The reciprocal manhattan distance of the row number of pixel in col i and pixel in col i+1 is used to calculate the transition probability. Furthermore, as we know that there won’t be a major unevenness n the boundary, the transition probability of pixels after a threshold of 10 is set to a very low value.
	
Using the Viterbi algorithm, we can better estimate a boundary as opposed to the Naive approach as here we take into account the smoothness of the boundary and hence including transition probabilities in our simple Bayes Net.

### Using HMM with Human Feedback:
For this approach, we have an extra set of information which are the coordinates of 2 pixels that lie on the air-ice ice-rock boundary respectively.
This is just a piece of additional information that we need to consider to estimate the boundaries, hence the emission and transition probabilities are the same.
The image is split at the column index of the coordinate, and we run the viterbi algorithm on these two images separately.
We get the boundary paths from both the images separately and merge them into a single path to finally plot the boundaries.


### Results:

![part2](https://media.github.iu.edu/user/18308/files/f63fa500-5491-11ec-919a-ac47e0abf5ea)



 
 
# Part 3: Reading Text

- In the problem, we make use of Simple Bayes Net to train our algorithm to detect handwritten/noisy text. 
- Our training sample consists of 26 Uppercase letters, 26 Lowercase letters, 10 digits, and 10 characters.
- Initially, we create a test dictionary using one of the noisy test images
- We basically make a matrix of blank spaces ‘  ‘ and asterisks ‘*’ to denote this character in the matrix format.
- We then compare each character of the testing string, pixel by pixel with each character of the training string and store the number of asterisks comparisons and  space comparisons for each character in the training string.
- Then we update our output dictionary storing the probability for each given character in the testing string.
- Now we extract and remove symbols and numbers separately from our main dictionary as symbols_dict and num_dict.
- We now have 3 dictionaries named num_dict, symbols_dict, and the original dictionary.
- We find the letter, symbol, and number with the highest probability from each dictionary respectively.
- There were some noisy images in which letters like l, t, J were detected as ‘1’.
- To resolve this, we set a certain threshold in order to avoid misidentification of such letters.
- Such thresholds were also set for noisy characters like ‘o’, ‘a’, ‘i’, ‘r’, ‘t’ where it would mark these as either ‘  ‘ or “ ‘ “.

### Output:
![Part3_output](https://media.github.iu.edu/user/18308/files/7404b000-5494-11ec-8ff5-35ccc54c0225)
# Assignment 3
## Team members: Ameya Dalvi, Henish Shah, Shubham Bhagat
# Part 1: Part-of-Speech Tagging

#### We have three major algorithms namely:
1. Simple (Simple Bayes Network)
2. HMM (Viterbi)
3. Complex (MCMC)

### Working:

#### 1.Simplified:
- For this algorithm, since the only connections are between the hidden variable and its corresponding observed variable, we directly calculate the posterior probabilities for each a tag given a word and take the maximum of those probabilities to predict the appropriate tag

#### 2.HMM (Viterbi):
- For this algorithm, we take into consideration the transition and emission probabilities. The main concept of this algorithm is dynamic programming. Thus, we make two tables to store the probability values and their corresponding tags.
- For the initial word, we just consider the initial probabilities (probabilities that a particular tag appears in the first word of a sentence) and the respective emission probabilities. For the following words, we firstly take into consideration the product of transition probabilities and the probabilities received in the previous column, and find the maximum product. Post that, that maximum product is multiplied with the emission probabilities of the current column and this process is repeated.
- Once our tables are ready, we start backtracking to find the best possible path/seq of the tags for a given sentence.

#### 3.Complex (MCMC)
- In this algorithm, we make use of Gibbs sampling method to generate 500 samples for each possible combination of tags for the words in a sentence. By this method, eventually with all the samples, the algorithm converges (tries to converge) on the best possible sequence of the tags. In addition to the emission and transition probabilities calculated in Viterbi, we also consider new set of emission and transition values in this algorithm.

### Silo Output:
![part1](https://media.github.iu.edu/user/18308/files/91397e80-5494-11ec-9443-bbedda4af977)



# Part 2: Ice Tracking
### Using Bayes Net:
- In this approach, we basically find the pixel with the least value in that column and assume it to be the boundary.
- The drawback of this naive approach is that it plots a boundary that is not continuous.
- Assuming that boundaries, in general, are a bit smoother and continuous in nature, having a model that takes into account these details would help in accurately denoting the boundary. 
- Hence to get a more accurate boundary detection we use HMM (Viterbi) in our 2nd approach.

### Using Viterbi Algorithm:
In this approach, we mainly focus on 3 types of probabilities.

1. **Initial Probability:**
Initial probability is calculated by assigning the reciprocal of the total number of rows for each pixel in the first column.
2. **Emission Probability:**
Emission probability is basically the pixel value divided by the sum of pixel values in that pixel column.
3. **Transition Probability:**
The reciprocal manhattan distance of the row number of pixel in col i and pixel in col i+1 is used to calculate the transition probability. Furthermore, as we know that there won’t be a major unevenness n the boundary, the transition probability of pixels after a threshold of 10 is set to a very low value.
	
Using the Viterbi algorithm, we can better estimate a boundary as opposed to the Naive approach as here we take into account the smoothness of the boundary and hence including transition probabilities in our simple Bayes Net.

### Using HMM with Human Feedback:
For this approach, we have an extra set of information which are the coordinates of 2 pixels that lie on the air-ice ice-rock boundary respectively.
This is just a piece of additional information that we need to consider to estimate the boundaries, hence the emission and transition probabilities are the same.
The image is split at the column index of the coordinate, and we run the viterbi algorithm on these two images separately.
We get the boundary paths from both the images separately and merge them into a single path to finally plot the boundaries.


### Results:

![part2](https://media.github.iu.edu/user/18308/files/f63fa500-5491-11ec-919a-ac47e0abf5ea)



 
 
# Part 3: Reading Text

- In the problem, we make use of Simple Bayes Net to train our algorithm to detect handwritten/noisy text. 
- Our training sample consists of 26 Uppercase letters, 26 Lowercase letters, 10 digits, and 10 characters.
- Initially, we create a test dictionary using one of the noisy test images
- We basically make a matrix of blank spaces ‘  ‘ and asterisks ‘*’ to denote this character in the matrix format.
- We then compare each character of the testing string, pixel by pixel with each character of the training string and store the number of asterisks comparisons and  space comparisons for each character in the training string.
- Then we update our output dictionary storing the probability for each given character in the testing string.
- Now we extract and remove symbols and numbers separately from our main dictionary as symbols_dict and num_dict.
- We now have 3 dictionaries named num_dict, symbols_dict, and the original dictionary.
- We find the letter, symbol, and number with the highest probability from each dictionary respectively.
- There were some noisy images in which letters like l, t, J were detected as ‘1’.
- To resolve this, we set a certain threshold in order to avoid misidentification of such letters.
- Such thresholds were also set for noisy characters like ‘o’, ‘a’, ‘i’, ‘r’, ‘t’ where it would mark these as either ‘  ‘ or “ ‘ “.

### Output:
![Part3_output](https://media.github.iu.edu/user/18308/files/7404b000-5494-11ec-8ff5-35ccc54c0225)
