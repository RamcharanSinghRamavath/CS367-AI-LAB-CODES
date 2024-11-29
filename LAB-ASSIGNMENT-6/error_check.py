import numpy as np

class hop_net:
    def __init__(self, size):
        self.size = size
        self.weights = np.zeros((size, size))

    def train(self, patterns):
        for p in patterns:
            self.weights += np.outer(p, p)
        np.fill_diagonal(self.weights, 0)
        self.weights /= len(patterns)

    def recall(self, pattern, steps=10):
        result = np.copy(pattern)
        for _ in range(steps):
            for i in range(self.size):
                activation = np.dot(self.weights[i], result)
                result[i] = 1 if activation >= 0 else -1
        return result

patterns = [np.array([1, -1, 1, -1, 1]), np.array([-1, 1, -1, 1, -1])]
test_pattern = np.array([1, -1, -1, -1, 1]) 

network = hop_net(size=5)
network.train(patterns)

output = network.recall(test_pattern)
print("Recalled Pattern:", output)
