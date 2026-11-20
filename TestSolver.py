import random
import solver

def legal_step(a, b):
    return tuple(b) in solver.neighbours(tuple(a))

def check(start):
    path = solver.solve(start)
    assert path is not None
    assert path[0] == list(start) and path[-1] == list(solver.GOAL)
    assert all(legal_step(a, b) for a, b in zip(path, path[1:]))
    return path

assert solver.solve(list(solver.GOAL)) == [list(solver.GOAL)]

p = check([7, 2, 4, 5, 0, 6, 8, 3, 1])
print("assignment start board:", len(p) - 1, "moves")

assert solver.solve([2, 1, 3, 4, 5, 6, 7, 8, 0])is None

random.seed(1)
for _ in range(200):
    state = list(solver.GOAL)
    k = random.randint(1, 14)
    for _ in range(k):
        state = list(random.choice(solver.neighbours(tuple(state))))
    assert len(check(state)) - 1 <= k

p = check([8, 6, 7, 2, 5, 4, 3, 0, 1])
assert len(p) - 1 == 31
print("hardest board: 31 moves (optimal)")
print("all tests passed")
