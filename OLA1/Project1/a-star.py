"""
**************************************************************************************************************************

Author: Timothy Morren
Date: 2/10/23
Course: Intro to AI (4350)
Professor: Joshua L. Phillips
Project: OLA1
Project Discription: Study the effects a heursitc has on the a-star algorithm
Project Files: a-star.py (current file), random-board.py 

**************************************************************************************************************************
"""



import heapq
import sys
import copy

class Set():
    def __init__(self):
        self.thisSet = set()

    def add(self, entry):
        if entry is not None:
            self.thisSet.add(entry.__hash__())

    def length(self):
        return len(self.thisSet)

    def isMember(self, query):
        return query.__hash__() in self.thisSet


class state():
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.tiles = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    def left(self):
        if (self.ypos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos - 1]
        s.ypos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s

    def right(self):
        if (self.ypos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos + 1]
        s.ypos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s

    def up(self):
        if (self.xpos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos - 1][s.ypos]
        s.xpos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s

    def down(self):
        if (self.xpos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos + 1][s.ypos]
        s.xpos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.tiles))

    def __eq__(self, other):
        if other is None:
            return False
        return self.tiles == other.tiles

    
    def __str__(self):
        return '%d %d %d\n%d %d %d\n%d %d %d\n' % (
            self.tiles[0][0], self.tiles[0][1], self.tiles[0][2],
            self.tiles[1][0], self.tiles[1][1], self.tiles[1][2],
            self.tiles[2][0], self.tiles[2][1], self.tiles[2][2])

    def copy(self):
        s = copy.deepcopy(self)
        return s


class PriorityQueue():
    def __init__(self):
        self.thisQueue = []

    def push(self, thisNode):
        heapq.heappush(self.thisQueue, (thisNode.val, -thisNode.id, thisNode))

    def pop(self):
        return heapq.heappop(self.thisQueue)[2]

    def isEmpty(self):
        return len(self.thisQueue) == 0

    def length(self):
        return len(self.thisQueue)

#Node class has a nodeid, val, state,parent node, and depth
nodeid = 0
class Node():
    def __init__(self, val, state, parent_node, depth):
        global nodeid
        self.id = nodeid
        nodeid += 1
        self.parent_node = parent_node
        self.depth = depth
        self.val = val
        self.state = state




def tree(start_state, h):
    goal_state = state()
    goal_state.tiles = [[0, 1, 2], [3, 4, 5], [6, 7, 8]] 
    frontier = PriorityQueue()
    closed_list = Set()
    start_node = Node(0,start_state,None,0)
    frontier.push(start_node)
    V = 0  #total number of nodes visited
    N = 0  #max number of nodes stored in mem
    d = 0  #depth
    while not frontier.isEmpty():
        if frontier.length() > N:
            N = frontier.length()
        current_node = frontier.pop()
        V += 1  #increment the node visited count
        if current_node.state == goal_state:
            d = current_node.depth #saves depth of solution path 
            return current_node, V, N, d
        expanded = expand(current_node, closed_list, goal_state, h) #
        for node in expanded:
            frontier.push(node)
    return None, V, N, d

def expand(current_node, closed_list, goal_state, h):
    closed_list.add(current_node.state)
    successors = []

    current_state = current_node.state
    right_child = current_state.right()
    left_child = current_state.left()
    up_child = current_state.up()
    down_child = current_state.down()
    children = [left_child, right_child, up_child, down_child]

    for child in children:
        if not closed_list.isMember(child) and child is not None:
            child = Node(0, child, None, current_node.depth + 1) 
            child.parent_node = current_node
            child.val = current_node.val + step(child, goal_state, h)
            successors.append(child)
    return successors


def step(child_node, goal_state, h):
    if h == "0":
        return 1
    if h == "1":
        return displaced_tiles(child_node.state, goal_state)
    if h == "2":
        return manhattan_distance(child_node.state, goal_state)
    if h == "3":
        return manhattan_distance_with_scaled_penalty(child_node.state, goal_state)
    
def displaced_tiles(current_state, goal_state):
    misplaced_tiles = 0
    for i in range(3):
        for j in range(3):
            if current_state.tiles[i][j] != goal_state.tiles[i][j]:
                misplaced_tiles += 1
    return misplaced_tiles

def manhattan_distance(current_state, goal_state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = current_state.tiles[i][j]
            if value != 0:  # Ignore the empty space (0)
                goal_i, goal_j = find_position(goal_state, value) #get the diference in the goal cord and the current cord
                distance += abs(i - goal_i) + abs(j - goal_j) #find how much the x cord is off and how much the y cord is off and add
    return distance

def find_position(state, value):
    for i in range(3):
        for j in range(3):
            if state.tiles[i][j] == value:
                return i, j

def manhattan_distance_with_scaled_penalty(current_state, goal_state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = current_state.tiles[i][j]
            if value != 0:  # Ignore the empty space (0)
                goal_i, goal_j = find_position(goal_state, value)
                tile_distance = abs(i - goal_i) + abs(j - goal_j)
                
                # Scale the penalty based on Manhattan distance
                penalty = max(0, tile_distance - 2) * 2
                
                distance += tile_distance + penalty
    return distance

def print_solution(solution_node):
    if solution_node is None:
        print("No solution found.")
        return

    path = []
    current_node = solution_node
    while current_node is not None:
        path.append(current_node.state)
        current_node = current_node.parent_node

    path.reverse()
    for state in path:
        print(state)

def main():
    start_state = state()
    inputs = []

    h = sys.argv[1]
    for line in sys.stdin:
        inputs += line.split()

    start_state.tiles = [
        [int(inputs[0]), int(inputs[1]), int(inputs[2])],
        [int(inputs[3]), int(inputs[4]), int(inputs[5])],
        [int(inputs[6]), int(inputs[7]), int(inputs[8])]
    ]


    #set 0s start position
    for i in range(3):
        for j in range(3):
            if start_state.tiles[i][j] == 0:
                start_state.xpos = i
                start_state.ypos = j
    solution_node, V, N, d = tree(start_state, h)
    if d>0:
        b=(V ** (1 / d))
    if d<=0:
        b=0
    print("V=" + str(V))
    print("N=" + str(N))
    print("d=" + str(d))
    print("b=" + "{:.5f}".format(b))
    print()

    print_solution(solution_node)

if __name__ == "__main__":
    main()


