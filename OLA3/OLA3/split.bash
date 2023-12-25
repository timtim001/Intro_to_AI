#!/bin/bash

# Ensure proper usage of the script
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <N> <command> <input_file>"
    exit 1
fi

N=$1
command=$2
input_file=$3

# Shuffle lines using sort -R
sort -R "$input_file" > temp.$$.txt

# Calculate number of lines for training data
total_lines=$(wc -l < temp.$$.txt)
train_lines=$((total_lines - N))

# Split into training and testing sets
head -n $train_lines temp.$$.txt > temp.$$.train.txt
tail -n $N temp.$$.txt > temp.$$.test.txt

# Execute command with split data
python3 "$command" temp.$$.train.txt temp.$$.test.txt

# Clean up temporary files
rm temp.$$.*
