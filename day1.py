def solve_safe_puzzle_part1(filename):
    """
    Solve the safe dial puzzle - Part 1.
    
    The dial has numbers 0-99 and starts at 50.
    L rotations go toward lower numbers (counterclockwise).
    R rotations go toward higher numbers (clockwise).
    The dial wraps around in both directions.
    
    Count how many times the dial points at 0 after any rotation.
    """
    # Read the rotations from the file
    with open(filename, 'r') as f:
        rotations = [line.strip() for line in f if line.strip()]
    
    # Start position
    position = 50
    count_zeros = 0
    
    # Process each rotation
    for rotation in rotations:
        direction = rotation[0]  # 'L' or 'R'
        distance = int(rotation[1:])  # The number after L/R
        
        if direction == 'L':
            # Left rotation: subtract distance (mod 100)
            position = (position - distance) % 100
        else:  # direction == 'R'
            # Right rotation: add distance (mod 100)
            position = (position + distance) % 100
        
        # Check if we landed on 0
        if position == 0:
            count_zeros += 1
    
    return count_zeros


def solve_safe_puzzle_part2(filename):
    """
    Solve the safe dial puzzle - Part 2 (Method 0x434C49434B).
    
    Count every time the dial points at 0 during OR at the end of a rotation.
    We need to count each click that lands on 0.
    """
    # Read the rotations from the file
    with open(filename, 'r') as f:
        rotations = [line.strip() for line in f if line.strip()]
    
    # Start position
    position = 50
    count_zeros = 0
    
    # Process each rotation
    for rotation in rotations:
        direction = rotation[0]  # 'L' or 'R'
        distance = int(rotation[1:])  # The number after L/R
        
        if direction == 'L':
            # Left rotation: going backwards from position
            # We click: position-1, position-2, ..., position-distance
            # We land on 0 when: (position - k) % 100 == 0, for k = 1 to distance
            # This happens when: k % 100 == position % 100
            
            # First time: k = position (if distance >= position and position > 0)
            # Then: k = position + 100, position + 200, etc.
            
            if position > 0 and distance >= position:
                # We hit 0 at click position, position+100, position+200, etc.
                count_zeros += 1 + (distance - position) // 100
            elif position == 0:
                # We're at 0, we won't hit it again until after 100 clicks
                count_zeros += distance // 100
            
            position = (position - distance) % 100
            
        else:  # direction == 'R'
            # Right rotation: going forward from position
            # We click: position+1, position+2, ..., position+distance
            # We land on 0 when: (position + k) % 100 == 0, for k = 1 to distance
            # This happens when: k % 100 == (100 - position) % 100
            
            if position > 0:
                # First time: k = 100 - position
                # Then: k = 100 - position + 100, etc.
                clicks_to_zero = 100 - position
                if distance >= clicks_to_zero:
                    count_zeros += 1 + (distance - clicks_to_zero) // 100
            else:  # position == 0
                # We're at 0, we won't hit it again until after 100 clicks
                count_zeros += distance // 100
            
            position = (position + distance) % 100
    
    return count_zeros

# Test with example first
print("Testing with example:")
test_result = solve_safe_puzzle_part2('test_example.txt')
print(f"Example result: {test_result} (should be 6)")
print()

# Solve the puzzle
password_part1 = solve_safe_puzzle_part1('input.txt')
print(f"Part 1 - The password is: {password_part1}")

password_part2 = solve_safe_puzzle_part2('input.txt')
print(f"Part 2 - The password is: {password_part2}")
