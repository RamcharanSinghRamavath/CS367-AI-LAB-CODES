import numpy as np
import random
import math

def distance_matrix(cities):
    num_cities = len(cities)
    dist_matrix = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            dist = np.linalg.norm(np.array(cities[i]) - np.array(cities[j]))
            dist_matrix[i][j] = dist_matrix[j][i] = dist
    return dist_matrix

def total_distance(tour, dist_matrix):
    distance = 0
    for i in range(len(tour) - 1):
        distance += dist_matrix[tour[i], tour[i + 1]]
    distance += dist_matrix[tour[-1], tour[0]]
    return distance

def generate_neighbor(tour):
    a, b = random.sample(range(len(tour)), 2)
    new_tour = tour[:]
    new_tour[a], new_tour[b] = new_tour[b], new_tour[a]
    return new_tour

def simulated_annealing(cities, initial_temp, cooling_rate, min_temp):
    num_cities = len(cities)
    dist_matrix = distance_matrix(cities)
    curr_tour = list(range(num_cities))
    random.shuffle(curr_tour)
    curr_dist = total_distance(curr_tour, dist_matrix)
    best_tour = curr_tour
    best_distance = curr_dist
    temperature = initial_temp
    
    while temperature > min_temp:
        new_tour = generate_neighbor(curr_tour)
        new_dist = total_distance(new_tour, dist_matrix)
        if new_dist < curr_dist:
            curr_tour, curr_dist = new_tour, new_dist
        else:
            acceptance_prob = math.exp(-(new_dist - curr_dist) / temperature)
            if random.random() < acceptance_prob:
                curr_tour, curr_dist = new_tour, new_dist
        if curr_dist < best_distance:
            best_tour, best_distance = curr_tour, curr_dist
        temperature *= cooling_rate
    
    return best_tour, best_distance

if __name__ == "__main__":
    cities = [
        [26.91, 75.78],  
        [24.58, 73.71],  
        [26.23, 73.02],  
        [26.91, 70.90],  
        [26.44, 74.63],  
        [27.20, 77.50],  
        [28.02, 73.31],  
        [25.21, 75.86],  
        [24.59, 72.71],  
        [24.88, 74.62]   
    ]
    
    initial_temp = 1000
    cooling_rate = 0.995
    min_temp = 1e-2
    best_tour, best_distance = simulated_annealing(cities, initial_temp, cooling_rate, min_temp)
    
    print("Best tour:", best_tour)
    print("Best distance:", best_distance)