import sys
import numpy.random as random


if (len(sys.argv) != 3):
    print()
    print("Usage: %s [seed] [number of random moves]" % (sys.argv[0]))
    print()
    sys.exit(1)

def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))


# There is no error checking in this code
# Well formatted input is assumed as well as
# proper processing given well-formed input

def main():
    inputs = []
    for line in sys.stdin:  
        inputs += line.split()
    
    goal = [
    [int(inputs[0]), int(inputs[1]), int(inputs[2])],
    [int(inputs[3]), int(inputs[4]), int(inputs[5])],
    [int(inputs[6]), int(inputs[7]), int(inputs[8])]
]
    # Just once
    rng = random.default_rng(int(sys.argv[1]))
    number_of_moves = int(sys.argv[2])
    board = goal
    zero_row = 0
    zero_col = 0  # location of 0
    # Can call this as many times as needed to generate moves...
    for x in range(number_of_moves):
        # These moves will be 0,1,2,3 which can each be
        # associated with a particular movement direction
        # (i.e. up, down, left, right).
        move = rng.integers(4)

        if move == 0:  # means moves zero left
            if zero_col > 0:  # makes sure 0 isn't on the left col
                temp = board[zero_row][zero_col - 1] #stores a temp
                board[zero_row][zero_col - 1] = 0
                board[zero_row][zero_col] = temp
                zero_col = zero_col - 1 #update zero

        elif move == 1:  # moves up
            if zero_row > 0:  # makes sure 0 isn't on the top
                temp = board[zero_row - 1][zero_col] #stores a temp
                board[zero_row - 1][zero_col] = 0
                board[zero_row][zero_col] = temp
                zero_row = zero_row - 1 #update zero


        elif move == 2:  # moves right
            if zero_col != 2:  # makes sure 0 isn't on the right col
                temp = board[zero_row][zero_col + 1] #stores a temp
                board[zero_row][zero_col + 1] = 0
                board[zero_row][zero_col] = temp
                zero_col = zero_col + 1 #update zero

        elif move == 3:  # moves down
            if zero_row != 2:  # makes sure 0 isn't on the bottom
                temp = board[zero_row + 1][zero_col] #stores a temp
                board[zero_row + 1][zero_col] = 0
                board[zero_row][zero_col] = temp
                zero_row = zero_row + 1 #update zero
                       
    print_board(board)
main()




