#!/bin/bash

counter=0  # Initialize the counter to 0

for i in {1..100}; do
    greedy_output=$(python3 greedy.py $i 1 5)
    sa_output=$(python3 SA.py $i 1 5)

    if [ "$(echo "$sa_output > $greedy_output" | bc -l)" -eq 1 ]; then
        ((counter++))
    fi
done

echo "SA was larger $counter times."


