import heapq

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

_GOAL_POS = {title: divmod(i, 3) for i, title in enumerate(GOAL)}

def manhattan(state):
    """Return the row + column distances of every title from its goal cell except the blank ones"""
    total = 0
    for i, title in enumerate(state):
        if title == 0:
            continue
        r, c = divmod(i, 3)
        gr, gc = _GOAL_POS[title]
        total += abs(r - gr) + abs(c - gc)
    return total

def neighbours(state):
    """Return every state reachable by sliding the blank one cell"""
    b = state.index(0)
    row, col = divmod(b, 3)
    targets = []
    if row > 0:
        targets.append(b - 3)
    if row < 2:
        targets.append(b + 3)
    if col > 0:
        targets.append(b - 1)
    if col < 2:
        targets.append(b + 1)

    results = []
    for t in targets:
        nxt = list(state)
        nxt[b], nxt[t] = nxt[t], nxt[b]
        results.append(tuple(nxt))
    return results

def is_solvable(state):
    """On a 3x3 board a state is solvable iff its inversion count is even."""
    tiles = [t for t in state if t != 0]
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions % 2 == 0

def solve(start):
    """ Return A* from 'start'. Return the list of states start...goal, or None"""
    start = tuple(start)
    if sorted(start) != list(range(9)) or not is_solvable(start):
        return None

    counter = 0
    frontier = [(manhattan(start), counter, start)]
    best_g = {start: 0}
    parent = {start: None}
    explored = set()

    while frontier:
        _,_, state =  heapq.heappop(frontier)

        if state in explored:
            continue
        if state == GOAL:
            return _build_path(parent, state)
        explored.add(state)

        g = best_g[state]
        for nxt in neighbours(state):
            new_g = g + 1
            if nxt not in best_g or new_g < best_g[nxt]:
                best_g[nxt] = new_g
                parent[nxt] = state
                counter += 1
                heapq.heappush(frontier, (new_g +manhattan(nxt), counter, nxt))
                
    return None

def _build_path(parent, state):
    path = []
    while state is not None:
        path.append(list(state))
        state = parent[state]
    path.reverse()
    return path

    
