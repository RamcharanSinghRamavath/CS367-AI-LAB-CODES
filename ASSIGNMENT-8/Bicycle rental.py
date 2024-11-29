import numpy as np
import random

# Define parameters for the Gbike problem
max_bikes = 20
max_move = 5
parking_cost = 4
move_cost = 2
free_move_cost = 1  # Free move by the employee
rental_price = 10  # Revenue per bike rented

# Expected values for requests and returns (Poisson distribution)
request1 = 3
request2 = 4
return1 = 3
return2 = 2

# Discount factor
gamma = 0.9

# Initialize state space (number of bikes at location 1 and 2)
states = [(i, j) for i in range(max_bikes + 1) for j in range(max_bikes + 1)]

# Reward function
def reward(state, action):
    s1, s2 = state
    move = action
    cost = 0
    
    # Move bikes between locations
    s1 -= move
    s2 += move

    # Apply parking cost if more than 10 bikes are kept overnight
    if s1 > 10:
        cost += parking_cost
    if s2 > 10:
        cost += parking_cost

    # Calculate the revenue from bike rentals
    revenue1 = min(s1, request1) * rental_price
    revenue2 = min(s2, request2) * rental_price
    revenue = revenue1 + revenue2

    # Calculate movement costs
    move_cost_total = abs(move) * move_cost
    if abs(move) == 1:  # Free move applies
        move_cost_total -= free_move_cost
    
    return revenue - (cost + move_cost_total)

# Transition function: simulates the next state based on customer requests and returns
def transition(state, action):
    s1, s2 = state
    
    # Move bikes according to action
    s1 -= action
    s2 += action

    # Handle bike requests (Poisson distribution)
    rented1 = min(s1, np.random.poisson(request1))
    rented2 = min(s2, np.random.poisson(request2))

    # Handle bike returns (Poisson distribution)
    returned1 = np.random.poisson(return1)
    returned2 = np.random.poisson(return2)

    # Update state based on bike movements, rentals, and returns
    s1_new = max(0, min(s1 - rented1 + returned1, max_bikes))
    s2_new = max(0, min(s2 - rented2 + returned2, max_bikes))
    
    return (s1_new, s2_new)

# Policy Iteration algorithm
def policy_iteration():
    # Initialize random policy and value function
    policy = {(i, j): random.randint(-max_move, max_move) for i in range(max_bikes + 1) for j in range(max_bikes + 1)}
    V = {(i, j): 0 for i in range(max_bikes + 1) for j in range(max_bikes + 1)}
    theta = 0.0001

    while True:
        # Policy Evaluation
        while True:
            delta = 0
            for state in states:
                old_v = V[state]
                action = policy[state]
                next_state = transition(state, action)
                V[state] = reward(state, action) + gamma * V[next_state]
                delta = max(delta, abs(old_v - V[state]))
            if delta < theta:
                break

        # Policy Improvement
        policy_stable = True
        for state in states:
            old_action = policy[state]
            best_action = None
            best_value = -float('inf')
            for action in range(-max_move, max_move + 1):
                next_state = transition(state, action)
                value = reward(state, action) + gamma * V[next_state]
                if value > best_value:
                    best_value = value
                    best_action = action
            policy[state] = best_action
            if old_action != best_action:
                policy_stable = False
        
        if policy_stable:
            break

    return policy, V

# Run policy iteration
policy, V = policy_iteration()

# Print the optimal policy and value function
print("Optimal Policy:")
for i in range(max_bikes + 1):
    for j in range(max_bikes + 1):
        print(f"State ({i},{j}): Move {policy[(i, j)]} bikes")

print("\nOptimal Value Function:")
for i in range(max_bikes + 1):
    for j in range(max_bikes + 1):
        print(f"State ({i},{j}): Value {V[(i, j)]}")
