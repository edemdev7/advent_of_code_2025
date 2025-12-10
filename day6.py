from math import prod
from pathlib import Path


def find_operation_row(lines: list[str]) -> int:
	"""Return the index of the row that holds the +/* operators."""

	for idx in range(len(lines) - 1, -1, -1):
		if any(ch in "+*" for ch in lines[idx]):
			return idx
	raise ValueError("No operation row found in worksheet")


def compute_totals(lines: list[str]) -> tuple[int, int]:
	"""Return grand totals for part 1 (row-wise) and part 2 (column-wise)."""

	if not lines:
		return 0, 0

	op_row_idx = find_operation_row(lines)
	relevant_lines = lines[: op_row_idx + 1]
	width = max(len(line) for line in relevant_lines)
	padded = [line.ljust(width) for line in relevant_lines]
	row_count = len(padded)

	def column_is_blank(col: int) -> bool:
		return all(row[col] == " " for row in padded)

	spans: list[tuple[int, int]] = []
	col = 0
	while col < width:
		while col < width and column_is_blank(col):
			col += 1
		if col >= width:
			break
		start = col
		while col < width and not column_is_blank(col):
			col += 1
		spans.append((start, col))

	part1_total = 0
	part2_total = 0

	for start, end in spans:
		numbers_part1: list[int] = []
		for row_idx in range(row_count - 1):
			chunk = padded[row_idx][start:end].strip()
			if chunk:
				numbers_part1.append(int(chunk))
		if not numbers_part1:
			raise ValueError("Encountered a problem with no row-wise numbers")

		op_segment = padded[-1][start:end]
		op_chars = [ch for ch in op_segment if ch in "+*"]
		if len(op_chars) != 1:
			raise ValueError("Invalid operator configuration in worksheet")
		operator = op_chars[0]

		if operator == "+":
			part1_total += sum(numbers_part1)
		else:
			part1_total += prod(numbers_part1)

		numbers_part2: list[int] = []
		for col_idx in range(end - 1, start - 1, -1):
			digits: list[str] = []
			for row_idx in range(row_count - 1):
				ch = padded[row_idx][col_idx]
				if ch.isdigit():
					digits.append(ch)
			if digits:
				numbers_part2.append(int("".join(digits)))
		if not numbers_part2:
			raise ValueError("Encountered a problem with no column-wise numbers")

		if operator == "+":
			part2_total += sum(numbers_part2)
		else:
			part2_total += prod(numbers_part2)

	return part1_total, part2_total


def main() -> None:
	input_path = Path(__file__).with_name("input.txt")
	lines = input_path.read_text().splitlines()
	part1_total, part2_total = compute_totals(lines)
	print(f"Part 1 - Grand total: {part1_total}")
	print(f"Part 2 - Grand total: {part2_total}")


if __name__ == "__main__":
	main()
