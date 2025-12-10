from collections import deque
from pathlib import Path
from typing import Dict, List, Set, Tuple

Grid = List[str]
Offsets = Tuple[Tuple[int, int], ...]


ADJACENT: Offsets = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
)


def read_grid(path: Path) -> Grid:
    """Return all non-empty rows of the puzzle input."""
    with path.open("r", encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def count_accessible_rolls(grid: Grid) -> int:
    """Count rolls of paper (@) that have fewer than four adjacent rolls."""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    accessible = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "@":
                continue
            neighbors = 0
            for dr, dc in ADJACENT:
                nr = r + dr
                nc = c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
                    neighbors += 1
            if neighbors < 4:
                accessible += 1
    return accessible


def total_removable_rolls(grid: Grid) -> int:
    """Simulate iterative removal of accessible rolls until stable."""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    rolls: Set[Tuple[int, int]] = {
        (r, c)
        for r in range(rows)
        for c in range(cols)
        if grid[r][c] == "@"
    }

    if not rolls:
        return 0

    adjacency: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
    neighbor_counts: Dict[Tuple[int, int], int] = {}

    for r, c in rolls:
        neighbors: List[Tuple[int, int]] = []
        for dr, dc in ADJACENT:
            nr = r + dr
            nc = c + dc
            if (nr, nc) in rolls:
                neighbors.append((nr, nc))
        adjacency[(r, c)] = neighbors
        neighbor_counts[(r, c)] = len(neighbors)

    queue: deque[Tuple[int, int]] = deque(
        pos for pos, count in neighbor_counts.items() if count < 4
    )
    removed: Set[Tuple[int, int]] = set()

    while queue:
        pos = queue.popleft()
        if pos in removed:
            continue
        removed.add(pos)
        for neighbor in adjacency[pos]:
            if neighbor in removed:
                continue
            neighbor_counts[neighbor] -= 1
            if neighbor_counts[neighbor] < 4:
                queue.append(neighbor)

    return len(removed)


def main(grid_path: str = "input.txt") -> None:
    grid = read_grid(Path(grid_path))
    part1 = count_accessible_rolls(grid)
    part2 = total_removable_rolls(grid)
    print(f"Part 1 - Accessible rolls: {part1}")
    print(f"Part 2 - Total removable rolls: {part2}")


if __name__ == "__main__":
    main()
