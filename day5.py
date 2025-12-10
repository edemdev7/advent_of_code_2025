from bisect import bisect_right
from pathlib import Path
from typing import List, Sequence, Tuple


Range = Tuple[int, int]


def parse_database(path: Path) -> Tuple[List[Range], List[int]]:
    """Parse the puzzle input into fresh ranges and available IDs."""
    raw = path.read_text().strip()
    try:
        range_block, ids_block = raw.split("\n\n", 1)
    except ValueError:  # pragma: no cover - puzzle input always has a blank line
        raise RuntimeError("Input must contain a blank line separating ranges and IDs")

    ranges: List[Range] = []
    for line in range_block.splitlines():
        line = line.strip()
        if not line:
            continue
        start_str, end_str = line.split("-")
        start = int(start_str)
        end = int(end_str)
        if end < start:
            start, end = end, start
        ranges.append((start, end))

    ids: List[int] = [int(line) for line in ids_block.splitlines() if line.strip()]
    return ranges, ids


def merge_ranges(ranges: Sequence[Range]) -> List[Range]:
    """Merge overlapping ranges so membership checks are fast."""
    if not ranges:
        return []
    sorted_ranges = sorted(ranges)
    merged: List[Range] = [sorted_ranges[0]]
    for start, end in sorted_ranges[1:]:
        m_start, m_end = merged[-1]
        if start <= m_end + 1:
            merged[-1] = (m_start, max(m_end, end))
        else:
            merged.append((start, end))
    return merged


def count_fresh_ids(ranges: Sequence[Range], ids: Sequence[int]) -> int:
    merged = merge_ranges(ranges)
    if not merged:
        return 0
    starts = [start for start, _ in merged]
    fresh = 0
    for value in ids:
        idx = bisect_right(starts, value) - 1
        if idx >= 0 and merged[idx][0] <= value <= merged[idx][1]:
            fresh += 1
    return fresh


def total_fresh_count(ranges: Sequence[Range]) -> int:
    """Return the total number of IDs covered by the fresh ranges."""
    merged = merge_ranges(ranges)
    return sum(end - start + 1 for start, end in merged)


def main() -> None:
    path = Path("input.txt")
    ranges, ids = parse_database(path)
    total_fresh = count_fresh_ids(ranges, ids)
    overall_fresh = total_fresh_count(ranges)
    print(f"Part 1 - Fresh ingredient IDs: {total_fresh}")
    print(f"Part 2 - Total IDs considered fresh: {overall_fresh}")


if __name__ == "__main__":
    main()
