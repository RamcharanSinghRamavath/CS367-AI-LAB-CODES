import random

class SATProblem:
    def __init__(self, n_variables, n_clauses):
        self.n_variables = n_variables
        self.n_clauses = n_clauses
        self.clauses = self.generate_random_3sat()

    def generate_random_3sat(self):
        clauses = []
        for _ in range(self.n_clauses):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, self.n_variables)
                literal = var if random.choice([True, False]) else -var
                clause.add(literal)
            clauses.append(clause)
        return clauses

    def is_satisfied(self, assignment):
        for clause in self.clauses:
            if not any(lit in assignment for lit in clause):
                return False
        return True

    def count_satisfied(self, assignment):
        sat_count = 0
        for clause in self.clauses:
            if any(lit in assignment for lit in clause):
                sat_count += 1
        return sat_count

def hill_climbing(sat_problem):
    assignment = {i for i in range(1, sat_problem.n_variables + 1) if random.random() < 0.5}
    best_count = sat_problem.count_satisfied(assignment)

    while True:
        improved = False
        for var in range(1, sat_problem.n_variables + 1):
            if var in assignment:
                new_assign = assignment - {var}
            else:
                new_assign = assignment | {var}

            new_count = sat_problem.count_satisfied(new_assign)
            if new_count > best_count:
                assignment = new_assign
                best_count = new_count
                improved = True

        if not improved:
            break

    return assignment, best_count

def beam_search(sat_problem, beam_width):
    curr_state = [{i for i in range(1, sat_problem.n_variables + 1) if random.random() < 0.5}]
    
    while curr_state:
        next_states = set()
        for state in curr_state:
            for var in range(1, sat_problem.n_variables + 1):
                new_state = state.copy()
                if var in new_state:
                    new_state.remove(var)
                else:
                    new_state.add(var)

                next_states.add(frozenset(new_state))

        scored_states = [(state, sat_problem.count_satisfied(state)) for state in next_states]
        scored_states.sort(key=lambda x: x[1], reverse=True)
        curr_state = {state for state, _ in scored_states[:beam_width]}

        for state, count in scored_states:
            if count == sat_problem.n_clauses:
                return state, count

    return None, 0

def var_neigh_desc(sat_problem):
    assignment = {i for i in range(1, sat_problem.n_variables + 1) if random.random() < 0.5}
    
    neigh_func = [
        lambda a: {v for v in a} ^ {random.choice(list(range(1, sat_problem.n_variables + 1)))},
        lambda a: {v for v in a} ^ {random.choice(list(range(1, sat_problem.n_variables + 1)))},
        lambda a: {random.choice(list(range(1, sat_problem.n_variables + 1))) for _ in range(random.randint(1, 3))}
    ]
    
    while True:
        improved = False
        for neighborhood_function in neigh_func:
            new_assign = neighborhood_function(assignment)
            new_count = sat_problem.count_satisfied(new_assign)
            if new_count > sat_problem.count_satisfied(assignment):
                assignment = new_assign
                improved = True
                break
        
        if not improved:
            break

    return assignment, sat_problem.count_satisfied(assignment)

if __name__ == "__main__":
    n_variables = int(input("Enter the number of variables: "))
    n_clauses = int(input("Enter the number of clauses: "))

    sat_problem = SATProblem(n_variables, n_clauses)

    print("Random 3-SAT Problem:")
    print("Clauses:", sat_problem.clauses)

    hc_solution, hc_count = hill_climbing(sat_problem)
    print("Hill Climbing Solution:", hc_solution, "Satisfied Clauses:", hc_count)

    beam_solution, beam_count = beam_search(sat_problem, beam_width=3)
    print("Beam Search Solution:", beam_solution, "Satisfied Clauses:", beam_count)

    vnd_solution, vnd_count = var_neigh_desc(sat_problem)
    print("Variable Neighborhood Descent Solution:", vnd_solution, "Satisfied Clauses:", vnd_count)