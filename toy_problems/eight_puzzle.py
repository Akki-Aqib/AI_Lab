"""
8-Puzzle Problem - Solved using A* Search Algorithm
Goal: Arrange tiles from 1-8 with blank(0) at end
"""
import heapq

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def manhattan_distance(state):
    distance = 0
    for i, val in enumerate(state):
        if val != 0:
            goal_pos = GOAL.index(val)
            distance += abs(i // 3 - goal_pos // 3) + abs(i % 3 - goal_pos % 3)
    return distance

def get_neighbors(state):
    neighbors = []
    idx = state.index(0)
    row, col = divmod(idx, 3)
    moves = [(-1,0,'Up'), (1,0,'Down'), (0,-1,'Left'), (0,1,'Right')]
    for dr, dc, direction in moves:
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = list(state)
            new_idx = nr * 3 + nc
            new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
            neighbors.append((tuple(new_state), direction))
    return neighbors

def a_star(start):
    heap = [(manhattan_distance(start), 0, start, [])]
    visited = set()
    while heap:
        f, g, state, path = heapq.heappop(heap)
        if state == GOAL:
            return path
        if state in visited:
            continue
        visited.add(state)
        for neighbor, direction in get_neighbors(state):
            if neighbor not in visited:
                new_g = g + 1
                new_f = new_g + manhattan_distance(neighbor)
                heapq.heappush(heap, (new_f, new_g, neighbor, path + [direction]))
    return None

def print_state(state, label=""):
    if label:
        print(f"\n{label}")
    for i in range(0, 9, 3):
        row = state[i:i+3]
        print(" ".join(str(x) if x != 0 else '_' for x in row))

if __name__ == "__main__":
    start = (1, 2, 3, 4, 0, 6, 7, 5, 8)
    print("=== 8-Puzzle Solver (A* Algorithm) ===")
    print_state(start, "Initial State:")
    print_state(GOAL, "Goal State:")

    solution = a_star(start)
    if solution:
        print(f"\nSolution found in {len(solution)} moves!")
        print("Moves:", " -> ".join(solution))
    else:
        print("No solution found.")
