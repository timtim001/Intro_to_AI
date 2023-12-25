import subprocess
import statistics
from concurrent.futures import ThreadPoolExecutor

# Function to execute the bash script and collect outputs
def execute_bash_script(script):
    output = subprocess.check_output(script, shell=True, text=True)
    return float(output.strip())  # Assuming the output is numeric

# Hardcoded array of values to loop through
replacement_values = [1,5,10]  # Modify this array with your desired values 1,5,10,25,50,75,100,125,140,145,149
num_runs = 100
results = {}

for value in replacement_values:
    bash_script = f"./split.bash {value} id3.py iris-data.txt"

    outputs = []
    with ThreadPoolExecutor() as executor:
        # Submit tasks to the executor
        futures = [executor.submit(execute_bash_script, bash_script) for _ in range(num_runs)]

        # Get the results as they are completed
        for future in futures:
            output_value = future.result()
            outputs.append(output_value)

    # Calculate mean and standard deviation of the outputs
    mean_value = (statistics.mean(outputs) / value) * 100
    std_deviation = statistics.stdev(outputs)
    std_deviation_percentage = (std_deviation / mean_value) * 100  # Standard deviation as a percentage

    # Store results
    results[value] = {'mean': mean_value, 'std_deviation': std_deviation, 'std_deviation_percentage': std_deviation_percentage}

# Display results
for value, data in results.items():
    mean_value = data['mean']
    std_deviation = data['std_deviation']
    std_deviation_percentage = data['std_deviation_percentage']

    print(f"For value {value}:")
    print(f"Mean: {mean_value} %")
    print(f"Standard Deviation (% of Mean): {std_deviation_percentage:.2f}%")
    print("------------------------")



