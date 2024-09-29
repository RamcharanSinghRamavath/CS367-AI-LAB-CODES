from collections import deque

def is_valid(state):
    le_mission, le_canni, ri_mission, ri_canni = state
    if le_mission > 0 and le_mission < le_canni:  
        return False
    if ri_mission > 0 and ri_mission < ri_canni: 
        return False
    return True

def get_next_states(state, le_boat):
    le_mission, le_canni, ri_mission, ri_canni = state
    if le_boat:
        moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]  
    else:
        moves = [(-1, 0), (-2, 0), (0, -1), (0, -2), (-1, -1)] 

    next_states = []
    for m, c in moves:
        new_state = (le_mission - m, le_canni - c, ri_mission + m, ri_canni + c) if le_boat else \
                    (le_mission + m, le_canni + c, ri_mission - m, ri_canni - c)
        if all(0 <= x <= 3 for x in new_state) and is_valid(new_state):
            next_states.append(new_state)
    return next_states

def bfs():
    state_ini = (3, 3, 0, 0)  
    goal_state = (0, 0, 3, 3)     
    le_boat = True
    queue = deque([(state_ini, le_boat, [])])  
    visited = set()

    while queue:
        state_curr, le_boat, path = queue.popleft()

        if state_curr == goal_state:
            return path + [state_curr]  

        visited.add((state_curr, le_boat))

        for next_state in get_next_states(state_curr, le_boat):
            if (next_state, not le_boat) not in visited:
                queue.append((next_state, not le_boat, path + [state_curr]))

    return None

solution = bfs()
print("Solution using with bfs:", solution)