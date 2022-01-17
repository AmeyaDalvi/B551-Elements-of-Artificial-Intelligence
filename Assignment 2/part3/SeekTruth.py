# SeekTruth.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDs HERE
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
from sklearn.feature_extraction.text import CountVectorizer
import math
import pdb
import re

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!

    dList = []
    tList = []
    for i in range(len(train_data["objects"])):
        if train_data["labels"][i] == "deceptive":
            dList.append(train_data["objects"][i])
        elif train_data["labels"][i] == "truthful":
            tList.append(train_data["objects"][i])

    vectorizer1 = CountVectorizer()
    vectorizer1.fit(dList)
    dDict = vectorizer1.vocabulary_


    vectorizer2 = CountVectorizer()
    vectorizer2.fit(tList)
    tDict = vectorizer2.vocabulary_


    prob_of_D = len(dList)/(len(dList)+len(tList))
    prob_of_T = len(tList)/(len(dList)+len(tList))

    count_line_D = {}
    for word in dDict.keys():
        if (re.match("[a-zA-Z]+", word)):
            count_line_D[word] = 0


    for i in count_line_D.keys():
        for line in dList:
            if i in line.lower():
                count_line_D[i] += 1
    
    count_line_T = {}
    for word in tDict.keys():
        if (re.match("[a-zA-Z]+", word)):
            count_line_T[word] = 0

    for i in count_line_T.keys():
        for line in tList:
            if i in line.lower():
                count_line_T[i] += 1
    
    
    prob_of_word_D = {}
    for i in count_line_D.keys():
        prob_of_word_D[i] = count_line_D[i]/len(dList)

    prob_of_word_T = {}
    for i in count_line_T.keys():
        prob_of_word_T[i] = count_line_T[i]/len(tList)


    results=[]
    i=0
    for line in test_data["objects"]:
        pd = prob_of_D
        pt = prob_of_T
        for word in line.lower().split(' '):
            if word in prob_of_word_D.keys() and word in prob_of_word_T.keys() :
                if (count_line_D[word] >10 or count_line_T[word] >10 ):
                    pd= pd*prob_of_word_D[word]
                    pt= pt*prob_of_word_T[word]
            # else: 
            #     pd= pd*0.5
            #     pt= pt*0.5
        prob_line = pd/(pd+pt)
        if prob_line >= 0.5:
            results.append("deceptive")
        else:
            results.append("truthful")
    

    return results
    # return [test_data["classes"][0]] * len(test_data["objects"])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.

    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}



    results= classifier(train_data, test_data_sanitized)
    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print(correct_ct)
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
