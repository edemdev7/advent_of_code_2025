def is_invalid_id_part1(num):
    """
    Check if a number is an invalid ID (Part 1).
    Invalid IDs are made of a sequence repeated exactly twice.
    E.g., 55 (5 twice), 6464 (64 twice), 123123 (123 twice)
    No leading zeroes allowed.
    """
    s = str(num)
    length = len(s)
    
    # Must have even length to be splittable into two equal parts
    if length % 2 != 0:
        return False
    
    # Split in half
    half = length // 2
    first_half = s[:half]
    second_half = s[half:]
    
    # Check if both halves are identical
    # Also check that first half doesn't have leading zero (which would make it invalid)
    if first_half == second_half and first_half[0] != '0':
        return True
    
    return False


def is_invalid_id_part2(num):
    """
    Check if a number is an invalid ID (Part 2).
    Invalid IDs are made of a sequence repeated at least twice.
    E.g., 55 (5 twice), 123123 (123 twice), 123123123 (123 three times)
    No leading zeroes allowed.
    """
    s = str(num)
    length = len(s)
    
    # Try all possible pattern lengths from 1 to length//2
    for pattern_len in range(1, length // 2 + 1):
        # Check if the length is divisible by pattern length
        if length % pattern_len == 0:
            pattern = s[:pattern_len]
            
            # Skip if pattern has leading zero
            if pattern[0] == '0':
                continue
            
            # Check if the entire string is this pattern repeated
            repetitions = length // pattern_len
            if repetitions >= 2 and pattern * repetitions == s:
                return True
    
    return False


def solve_gift_shop(filename, part=1):
    """
    Find all invalid product IDs in the given ranges and sum them.
    """
    # Read the input
    with open(filename, 'r') as f:
        content = f.read().strip()
    
    # Parse the ranges
    ranges = []
    for range_str in content.split(','):
        range_str = range_str.strip()
        if range_str:
            parts = range_str.split('-')
            start = int(parts[0])
            end = int(parts[1])
            ranges.append((start, end))
    
    total = 0
    invalid_ids = []
    
    # Choose the appropriate validation function
    is_invalid = is_invalid_id_part1 if part == 1 else is_invalid_id_part2
    
    # Check each range
    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid(num):
                invalid_ids.append(num)
                total += num
    
    return total, invalid_ids


# Solve Part 1
total1, invalid_ids1 = solve_gift_shop('input.txt', part=1)
print(f"Part 1 - Sum of all invalid IDs: {total1}")
print(f"Found {len(invalid_ids1)} invalid IDs")

# Solve Part 2
total2, invalid_ids2 = solve_gift_shop('input.txt', part=2)
print(f"\nPart 2 - Sum of all invalid IDs: {total2}")
print(f"Found {len(invalid_ids2)} invalid IDs")
