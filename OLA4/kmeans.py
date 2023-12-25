"""
**************************************************************************************************************************

Author: Timothy Morren
Date: 08/12/23
Course: Intro to AI (4350)
Professor: Joshua L. Phillips
Project: OLA4
Project Discription: Develop a software agent in Python to perform K-means clustering on labeled classification data.
Project Files: kmeans.py report.pdf

**************************************************************************************************************************
"""
import sys
import numpy as np

def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b)**2))

def k_means_clustering(training_data, validation_data, num_clusters):
    # Reading training data
    with open(training_data, 'r') as file:
        lines = file.readlines()
        training_examples = np.array([list(map(float, line.strip().split()[:-1])) for line in lines])

    #reading validation data
    with open(validation_data, 'r') as file:
        lines = file.readlines()
        validation_examples = np.array([list(map(float, line.strip().split()[:-1])) for line in lines])

    #Initialization: selecting first K examples as centroids
    centroids = training_examples[:num_clusters]

    while True:
        #each training example to the closest centroid
        clusters = [[] for _ in range(num_clusters)] #cool python array creation
        for example in training_examples:
            distances = [euclidean_distance(example, centroid) for centroid in centroids]
            closest_centroid_idx = np.argmin(distances) #smallest distance
            clusters[closest_centroid_idx].append(example)

        #update centers
        new_centroids = np.array([np.mean(cluster, axis=0) if cluster else centroid for centroid, cluster in zip(centroids, clusters)])

        #check convergence
        if np.array_equal(centroids, new_centroids):
            break
        centroids = new_centroids

    #assign labels to clusters based on majority vote
    cluster_labels = []
    for cluster in clusters:
        if not cluster:
            cluster_labels.append(-1)  #Assign a placeholder labe for empty cluster
            continue
        labels, counts = np.unique(np.array(cluster)[:, -1].astype(int), return_counts=True)
        majority_label = labels[np.argmax(counts)]
        cluster_labels.append(majority_label)

    #lassify validation data and count correctly classified example
    correctly_classified = 0
    for example in validation_examples:
        distances = [euclidean_distance(example, centroid) for centroid in centroids]
        closest_centroid_idx = np.argmin(distances)
        if cluster_labels[closest_centroid_idx] == int(example[-1]):
            correctly_classified += 1

    return correctly_classified


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python kmeans_classification.py <num_clusters> <training_data_filename> <validation_data_filename>")
    else:
        num_clusters = int(sys.argv[1])
        training_data_filename = sys.argv[2]
        validation_data_filename = sys.argv[3]

        correct_classifications = k_means_clustering(training_data_filename, validation_data_filename, num_clusters)
        print(correct_classifications)
