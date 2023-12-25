import sys
import re
import statistics


# Initialize lists to store the values
v_values = []
n_values = []
d_values = []
b_values = []

# Regular expression patterns to match V, N, d, and b lines
v_pattern = re.compile(r"V=(\d+)")
n_pattern = re.compile(r"N=(\d+)")
d_pattern = re.compile(r"d=(\d+)")
b_pattern = re.compile(r"b=(\d+\.\d+)")

# Loop through each line of input
for line in sys.stdin:
    # Match V, N, d, and b lines
    v_match = v_pattern.search(line)
    n_match = n_pattern.search(line)
    d_match = d_pattern.search(line)
    b_match = b_pattern.search(line)

    if v_match:
        v_values.append(int(v_match.group(1)))
    if n_match:
        n_values.append(int(n_match.group(1)))
    if d_match:
        d_values.append(int(d_match.group(1)))
    if b_match:
        b_values.append(float(b_match.group(1)))

# Check if any of the lists are empty
if not v_values or not n_values or not d_values or not b_values:
    print("No valid data found in the input.")
else:
    # Calculate statistics
    v_min = min(v_values)
    v_median = statistics.median(v_values)
    v_mean = statistics.mean(v_values)
    v_max = max(v_values)
    v_stddev = statistics.stdev(v_values)

    n_min = min(n_values)
    n_median = statistics.median(n_values)
    n_mean = statistics.mean(n_values)
    n_max = max(n_values)
    n_stddev = statistics.stdev(n_values)

    d_min = min(d_values)
    d_median = statistics.median(d_values)
    d_mean = statistics.mean(d_values)
    d_max = max(d_values)
    d_stddev = statistics.stdev(d_values)

    b_min = min(b_values)
    b_median = statistics.median(b_values)
    b_mean = statistics.mean(b_values)
    b_max = max(b_values)
    b_stddev = statistics.stdev(b_values)

    # Print the calculated statistics
    print(f"V - Minimum: {v_min}, Median: {v_median}, Mean: {v_mean}, Maximum: {v_max}, Standard Deviation: {v_stddev}")
    print(f"N - Minimum: {n_min}, Median: {n_median}, Mean: {n_mean}, Maximum: {n_max}, Standard Deviation: {n_stddev}")
    print(f"d - Minimum: {d_min}, Median: {d_median}, Mean: {d_mean}, Maximum: {d_max}, Standard Deviation: {d_stddev}")
    print(f"b - Minimum: {b_min}, Median: {b_median}, Mean: {b_mean}, Maximum: {b_max}, Standard Deviation: {b_stddev}")


