from collections import deque
import numpy as np
import random

class Node:
    def __init__(self, state, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.depth = depth

def get_successors(node):
    successors = []
    index = node.state.index(0)
    moves = []
    if index >= 3:  
        moves.append(-3)
    if index < 6:  
        moves.append(3)
    if index % 3 > 0:  
        moves.append(-1)
    if index % 3 < 2:  
        moves.append(1)

    for move in moves:
        new_index = index + move
        new_state = list(node.state)
        new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
        successor = Node(new_state, node, node.depth + 1)
        successors.append(successor)
    
    return successors

def dls(node, goal_state, depth_limit):
    if node.state == goal_state:
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]

    if node.depth >= depth_limit:
        return None

    for successor in get_successors(node):
        result = dls(successor, goal_state, depth_limit)
        if result:
            return result

    return None

def depth_limited_search(start_state, goal_state, depth_limit):
    start_node = Node(start_state)
    return dls(start_node, goal_state, depth_limit)
start_state = [1, 2, 3, 4, 5, 6, 7, 0, 8]  #  start state
goal_state = [1, 2, 3, 4, 5, 6, 0, 7, 8]   #  goal state

depth_limit = 10

solution = depth_limited_search(start_state, goal_state, depth_limit)

if solution:
    print("Solution found within depth limit:")
    for step in solution:
        print(step)
else:
    print(f"No solution found within depth limit {depth_limit}.")
