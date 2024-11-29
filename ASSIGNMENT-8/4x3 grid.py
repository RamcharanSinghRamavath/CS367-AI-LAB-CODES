import numpy as np

# Define the environment
n_rows, n_cols = 4, 3
goal_states = [(0, 2), (3, 2)]  # Goal states with +1 and -1 reward respectively

# Rewards for each state
def reward(s, reward_type):
    if s in goal_states:
        return 1 if s == (0, 2) else -1  # Reward for goal states
    else:
        return reward_type  # Default reward for other states

# Actions mapping
actions = {
    'U': (-1, 0),  # Up
    'D': (1, 0),   # Down
    'L': (0, -1),  # Left
    'R': (0, 1)    # Right
}

# Transition function considering stochasticity
def transition(s, a):
    prob = 0.8
    # 20% chance to go to a perpendicular direction
    if np.random.rand() < prob:
        dx, dy = actions[a]  # Intended action
    else:
        # Random perpendicular direction
        perpendicular_actions = ['U', 'D', 'L', 'R']
        perpendicular_actions.remove(a)  # Remove the intended action
        new_a = np.random.choice(perpendicular_actions)
        dx, dy = actions[new_a]
    
    new_s = (max(0, min(s[0] + dx, n_rows - 1)), 
             max(0, min(s[1] + dy, n_cols - 1)))
    return new_s

# Value Iteration algorithm
def value_iteration(reward_type, gamma=0.9, theta=0.0001):
    # Initialize value function to zero for all states
    V = np.zeros((n_rows, n_cols))
    
    # Value Iteration loop
    while True:
        delta = 0
        # Iterate over all states
        for i in range(n_rows):
            for j in range(n_cols):
                state = (i, j)
                if state in goal_states:
                    continue  # Skip goal states
                old_v = V[i, j]
                # Update the value for the state by considering all actions
                action_values = []
                for action in actions:
                    next_state = transition(state, action)
                    reward_val = reward(state, reward_type)
                    action_value = reward_val + gamma * V[next_state]
                    action_values.append(action_value)
                # Update the state value to the maximum action value
                V[i, j] = max(action_values)
                delta = max(delta, abs(old_v - V[i, j]))
        
        # Convergence check
        if delta < theta:
            break
    
    return V

# Run Value Iteration for different reward types
reward_types = [-2, 0.1, 0.02, 1]
for r_type in reward_types:
    V = value_iteration(r_type)
    print(f"Value Function for reward type {r_type}:")
    print(V)