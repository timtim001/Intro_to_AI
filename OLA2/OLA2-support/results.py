import subprocess
import numpy as np

# Define the number of runs
num_runs = 100

# Initialize counters for SA and Greedy wins/ties
sa_wins = 0
greedy_wins = 0
ties = 0

tolerance = 1e-8  # Set the tolerance value

for i in range(num_runs):
    sa_result = subprocess.check_output(["python", "sa.py", str(i), "5", "100"], universal_newlines=True)
    greedy_result = subprocess.check_output(["python", "Greedy.py", str(i), "5", "100"], universal_newlines=True)

    sa_point = [float(x) for x in sa_result.split()]
    greedy_point = [float(x) for x in greedy_result.split()]

    # Check if the absolute difference between the points is within the tolerance
    if all(abs(a - b) <= tolerance for a, b in zip(sa_point, greedy_point)):
        ties += 1
    elif all(a > b for a, b in zip(sa_point, greedy_point)):
        sa_wins += 1
    else:
        greedy_wins += 1

print(f"SA Wins: {sa_wins}")
print(f"Greedy Wins: {greedy_wins}")
print(f"Ties: {ties}")

