import random

def gen_k_sat(k, m, n):
    variables = [f"x{i + 1}" for i in range(n)]
    k_sat_formula = []

    for _ in range(m):
        clause_vars = random.sample(variables, k)
        clause = []
        
        for var in clause_vars:
            if random.choice([True, False]):
                clause.append(f"¬{var}")
            else:
                clause.append(var)

        k_sat_clause = " v ".join(clause)
        k_sat_formula.append(f"({k_sat_clause})")

    k_sat_problem = " ∧ ".join(k_sat_formula)
    return k_sat_problem

if __name__ == "__main__":
    k = int(input("Enter k: "))
    m = int(input("Enter m: "))
    n = int(input("Enter n: "))

    k_sat_instance = gen_k_sat(k, m, n)
    print("\nRandom k-SAT Problem:")
    print(k_sat_instance)