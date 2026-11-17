from collections import deque

# breadth-first search (BFS)
# returns cells visited and shortest path
def bfs(grid, start, end):
    rows = len(grid)
    cols = len(grid[0])

    queue = deque([start]) # cells to be explored
    visited = {start} # cells already explored
    previous = {} # remember the previous cell for each visited cell

    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    exploration_order = []

    while queue:
        current = queue.popleft()
        exploration_order.append(current)

        # stop at destination
        if current == end:
            break

        row, col = current

        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc

            neighbor = (new_row, new_col)

            if not (0<=new_row<rows and 0<=new_col<cols):
                continue

            if grid[new_row][new_col] or neighbor in visited:
                continue

            visited.add(neighbor)
            previous[neighbor] = current
            queue.append(neighbor)

    # return shortest path
    path = []

    if end in visited:
        current = end

        while current != start:
            path.append(current)
            current = previous[current]

        path.append(start)
        path.reverse()

    return exploration_order, path