import sys
import numpy as np
import matplotlib.pyplot as plt
import tempfile
import os
import subprocess
import multiprocessing

def load_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        data = [list(map(float, line.strip().split()[:-1])) for line in lines]
    return np.array(data)

def split_data(data, m):
    np.random.shuffle(data)
    return data[m:], data[:m]

def save_data_to_file(data, filename):
    with open(filename, 'w') as file:
        for row in data:
            file.write(' '.join(map(str, row)) + '\n')

def average_accuracy(num_clusters, data, m=10, iterations=100):
    accuracies = []
    for _ in range(iterations):
        train_data, val_data = split_data(data, m)
        
        # Create temporary files for training and validation data
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as train_file, tempfile.NamedTemporaryFile(mode='w', delete=False) as val_file:
            train_filename = train_file.name
            val_filename = val_file.name
            save_data_to_file(train_data, train_filename)
            save_data_to_file(val_data, val_filename)

        # Run kmeans.py using subprocess
        result = subprocess.run(['python', 'kmeans.py', str(num_clusters), train_filename, val_filename], stdout=subprocess.PIPE, text=True)
        
        # Parse the output to get the number of correctly classified cases
        num_correct = int(result.stdout.strip())  # Assuming the output is the number of correctly classified cases
        accuracy = num_correct / m  # Calculate accuracy
        accuracies.append(accuracy)

        # Delete temporary files
        os.remove(train_filename)
        os.remove(val_filename)

    return np.mean(accuracies)
def calculate_error(accuracies):
    mean_accuracy = np.mean(accuracies)
    std_error = 1.96 * np.std(accuracies) / np.sqrt(len(accuracies))
    return mean_accuracy, std_error

def compute_accuracies(num_clusters, data):
    accuracies = []
    for _ in range(100):  # 100 random shuffles
        np.random.shuffle(data)
        train_data, val_data = split_data(data, 10)
        train_data = train_data[:-10]  # n - 10 training set size
        accuracy = average_accuracy(num_clusters, train_data, m=10, iterations=1)  # Using a validation set of size 10
        accuracies.append(accuracy)
    return accuracies

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test.py <data_filename>")
    else:
        data_filename = sys.argv[1]

        data = load_data(data_filename)
        total_examples = len(data)

        cluster_range = range(1, 141)  # Assuming clusters range from 1 to 4, modify if needed

        pool = multiprocessing.Pool()  # Initialize a pool of workers

        results = pool.starmap(compute_accuracies, [(num_clusters, data) for num_clusters in cluster_range])
        pool.close()
        pool.join()

        mean_accuracies = []
        std_errors = []
        for accuracies in results:
            mean_accuracy, std_error = calculate_error(accuracies)
            mean_accuracies.append(mean_accuracy * 100)  # Convert to percentage
            std_errors.append(std_error * 100)  # Convert to percentage

        # Plotting the mean performance with error bars
        plt.figure(figsize=(8, 6))
        plt.errorbar(list(cluster_range), mean_accuracies, yerr=std_errors, fmt='o-', ecolor='orange', capsize=5)
        plt.title('Mean Performance vs. Number of Clusters (K)')
        plt.xlabel('Number of Clusters (K)')
        plt.ylabel('Mean Accuracy (%)')
        plt.grid(True)
        plt.show()