"""
**************************************************************************************************************************

Author: Timothy Morren
Date: 17/11/23
Course: Intro to AI (4350)
Professor: Joshua L. Phillips
Project: OLA3
Project Discription: Create an ID3 decision tree from labeled classification data.
Project Files: id3.py

**************************************************************************************************************************
"""
import numpy as np
import sys

#node is the root of the tree with left and right nodes (sub-trees)
class Node:
    def __init__(self, attribute=None, split_point=None, left=None, right=None, label=None):
        self.attribute = attribute #stores current node attribute (column of the data)
        self.split_point = split_point #stores current nodes split point
        self.left = left #current nodes left sub-tree (node)
        self.right = right #current nodes right sub-tree (node)
        self.label = label 

    #calculate the entropy of a set of data
def entropy(data):
    unique_labels, counts = np.unique(data, return_counts=True)
    probabilities = counts / len(data)
    entropy_value = -np.sum(probabilities * np.log2(probabilities))
    return entropy_value

    #calculate information gain for a given attribute and split point
def information_gain(examples, attribute, split_point):
    total_entropy = entropy(examples[:, -1])

    #split the examples based on the given attribute and split point
    left_subset = examples[examples[:, attribute] <= split_point][:, -1]
    right_subset = examples[examples[:, attribute] > split_point][:, -1]

    #weighted sum of entropies for the subsets
    weighted_entropy = (len(left_subset) / len(examples)) * entropy(left_subset) + (len(right_subset) / len(examples)) * entropy(right_subset)


    information_gain_value = total_entropy - weighted_entropy
    return information_gain_value

def find_best_split(examples, attributes):
    best_attribute = None
    best_split_point = None
    max_information_gain = -1

    for attribute in sorted(attributes):  #Sort attributes to ensure left-to-right order
        unique_values = np.unique(examples[:, attribute])
        for value in np.sort(unique_values):  # Sort values for smallest to largest
            information_gain_value = information_gain(examples, attribute, value)
            if information_gain_value > max_information_gain:
                max_information_gain = information_gain_value
                best_attribute = attribute
                best_split_point = value
            elif information_gain_value == max_information_gain:
                #if the information gain is equal, break the tie using attribute order than value
                if (attribute < best_attribute) or (attribute == best_attribute and value < best_split_point):
                    best_attribute = attribute
                    best_split_point = value

    return best_attribute, best_split_point


def decision_tree_learning(examples, attributes, default=None):
    if len(set(examples[:, -1])) == 1:
        #if all examples have the same label, return a leaf node
        return Node(label=examples[0, -1])
    if len(examples) == 0:
    #case when examples is empty
        return Node(label=default) 
    if len(attributes) == 0:
        #if no attributes left, return a leaf node with the most common label
        return Node(label=np.argmax(np.bincount(examples[:, -1].astype(int))))

    #find the best split point
    best_attribute, best_split_point = find_best_split(examples, attributes)

    if best_attribute is None or best_split_point is None:
        #if no best attribute or split point found, return a leaf node with the most common label
        return Node(label=np.argmax(np.bincount(examples[:, -1].astype(int))))

    #create a node with the best attribute and split point
    node = Node(attribute=best_attribute, split_point=best_split_point)

    #recursively build the left and right subtrees
    left_examples = examples[examples[:, best_attribute] <= best_split_point]
    right_examples = examples[examples[:, best_attribute] > best_split_point]

    left_node = decision_tree_learning(left_examples, attributes - {best_attribute})
    right_node = decision_tree_learning(right_examples, attributes - {best_attribute})

    node.left = left_node
    node.right = right_node

    return node


def classify_example(example, tree, default_value=None):
    if tree.label is not None:
        return tree.label
    else:
        if tree.split_point is not None:
            if example[tree.attribute] <= tree.split_point:
                return classify_example(example, tree.left, default_value)
            else:
                return classify_example(example, tree.right, default_value)
        else:
            return default_value




def main():
    if len(sys.argv) != 3:
        print("Usage: python id3.py <training data filename> <validation data filename>.")
        sys.exit(1)

    fileName = sys.argv[1]
    training_data = np.loadtxt(fileName)
    fileName = sys.argv[2]
    validation_data = np.loadtxt(fileName)

    #Create the arrays for validations and training data
    if len(validation_data.shape) < 2:
        validation_data = np.array([validation_data])

    if len(training_data.shape) < 2:
        training_data = np.array([training_data])

    #decision_tree_learning to build the decision tree
    attributes = set(range(training_data.shape[1] - 1))
    root = decision_tree_learning(training_data, attributes)

    #classify the validation examples using the decision tree
    correct_classifications = 0
    for example in validation_data:
        predicted_label = classify_example(example, root)
        actual_label = example[-1]
        if predicted_label == actual_label:
            correct_classifications += 1

    #output the number of correctly classified examples
    print(correct_classifications)

if __name__ == "__main__":
    main()

