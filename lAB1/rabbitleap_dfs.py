def rableap_dfs(ini_state, fin_state):
    stack = [(ini_state, [])]  
    visited = set()
    visited.add(tuple(ini_state))

    while stack:
        state, path = stack.pop()
        if state == fin_state:
            return path + [state]

        for new_state in moves(state):
            if tuple(new_state) not in visited:
                visited.add(tuple(new_state))
                stack.append((new_state, path + [state]))

    return None

def moves(state):
    empty_index = state.index('_')
    possible_states = []
    moves = [(-1, 1), (-2, 2)]
    
    for move in moves:
        for direction in move:
            new_index = empty_index + direction
            if 0 <= new_index < len(state):
                new_state = state[:]
                new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
                possible_states.append(new_state)

    return possible_states

ini_state = ['E', 'E', 'E', '_', 'W', 'W', 'W']
fin_state = ['W', 'W', 'W', '_', 'E', 'E', 'E']

dfs_solution = rableap_dfs(ini_state, fin_state)
print("\nSolution using with dfs:")
for step in dfs_solution:
    print(step)