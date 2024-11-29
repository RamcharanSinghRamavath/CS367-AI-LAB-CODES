import numpy as np

class rook_hop:
    def __init__(self, size=8):
        self.size = size
        self.weights = np.zeros((size, size))

    def initialize_weights(self):
        for i in range(self.size):
            for j in range(self.size):
                if i != j:
                    self.weights[i][j] = -1

    def optimize(self, initial_state, steps=10):
        state = np.copy(initial_state)
        for _ in range(steps):
            for i in range(self.size):
                activation = np.dot(self.weights[i], state)
                state[i] = 1 if activation > 0 else -1
        return state

initial_state = np.random.choice([-1, 1], size=(8,))
eight_rook = rook_hop(size=8)
eight_rook.initialize_weights()
final_state = eight_rook.optimize(initial_state)
print("Final State:", final_state)
