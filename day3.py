from pathlib import Path
from typing import Iterable, List


def parse_banks(path: Path) -> List[str]:
    """Return all non-empty battery bank rows from the input file."""
    with path.open("r", encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def max_bank_joltage(bank: str, picks: int) -> int:
    """Compute the largest value by activating exactly *picks* batteries."""
    digits = [int(ch) for ch in bank]
    if len(digits) < picks:
        raise ValueError("Bank does not contain enough batteries for the request")

    to_remove = len(digits) - picks
    stack: List[int] = []
    for digit in digits:
        while to_remove and stack and stack[-1] < digit:
            stack.pop()
            to_remove -= 1
        stack.append(digit)

    if to_remove:
        stack = stack[:-to_remove]

    selected = stack[:picks]
    value = 0
    for digit in selected:
        value = value * 10 + digit
    return value


def total_output_joltage(banks: Iterable[str], picks: int) -> int:
    """Sum the maximum joltage from every provided bank."""
    return sum(max_bank_joltage(bank, picks) for bank in banks)


def run_example() -> None:
    example_banks = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111",
    ]
    part1_expected = 357
    part2_expected = 3_121_910_778_619
    part1_result = total_output_joltage(example_banks, picks=2)
    part2_result = total_output_joltage(example_banks, picks=12)
    print(f"Example part 1: {part1_result} (expected {part1_expected})")
    print(f"Example part 2: {part2_result} (expected {part2_expected})")


def main() -> None:
    input_path = Path("input.txt")
    banks = parse_banks(input_path)
    part1_total = total_output_joltage(banks, picks=2)
    part2_total = total_output_joltage(banks, picks=12)
    print(f"Part 1 - Total output joltage: {part1_total}")
    print(f"Part 2 - Total output joltage: {part2_total}")


if __name__ == "__main__":
    run_example()
    main()
