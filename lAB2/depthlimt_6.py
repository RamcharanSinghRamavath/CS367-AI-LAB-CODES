from collections import deque
import random
import time
import tracemalloc

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

def get_successors(node):
    successors = []
    index = node.state.index(0)
    moves = []
    if index // 3 == 0:
        moves = [3]
    elif index // 3 == 1:
        moves = [-3, 3]
    elif index // 3 == 2:
        moves = [-3]
    
    if index % 3 == 0:
        moves.append(1)
    elif index % 3 == 1:
        moves += [-1, 1]
    elif index % 3 == 2:
        moves.append(-1)

    for move in moves:
        im = index + move
        if 0 <= im < 9:
            new_state = list(node.state)
            new_state[index], new_state[im] = new_state[im], new_state[index]
            successors.append(Node(new_state, node))
    return successors

def bfs(start_state, goal_state):
    start_node = Node(start_state)
    queue = deque([start_node])
    visited = set()
    nodes_explored = 0

    while queue:
        node = queue.popleft()
        if tuple(node.state) in visited:
            continue
        visited.add(tuple(node.state))
        nodes_explored += 1
        if node.state == goal_state:
            path = []
            while node:
                path.append(node.state)
                node = node.parent
            return path[::-1], nodes_explored
        for successor in get_successors(node):
            queue.append(successor)

    return None, nodes_explored

def generate_goal_state(depth):
    start_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    s_node = Node(start_state)
    for _ in range(depth):
        s_node = random.choice(get_successors(s_node))
    return s_node.state

def run_experiment(max_depth):
    print(f"{'Depth':<10}{'Time (s)':<15}{'Nodes Explored':<20}{'Memory (KB)':<15}")
    for d in range(1, max_depth + 1):
        start_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        goal_state = generate_goal_state(d)
        
        tracemalloc.start()
        start_time = time.time()
        solution, nodes_explored = bfs(start_state, goal_state)
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        time_taken = end_time - start_time
        print(f"{d:<10}{time_taken:<15.6f}{nodes_explored:<20}{peak / 1024:<15.2f}")

run_experiment(20)
