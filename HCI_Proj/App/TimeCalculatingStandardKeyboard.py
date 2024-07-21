# Define time constants
T_RIGHT = 0.6
T_LEFT = 0.6
T_BLINK = 1.5


keyboard_layout = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Backspace"],
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "Enter"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l", "?"],
    ["z", "x", "c", "v", "b", "n", "m", ",", ".", "!", "Caps Lock"]
]


# Helper function to find the position of a letter in a layout
def find_position(layout, letter):
    for row_idx, row in enumerate(layout):
        if letter in row:
            return (row_idx, row.index(letter))
    return None

def time_within_quadrant_right_path(layout, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    total_time = 0
    current_row, current_col = start_row, start_col
    total_rows = len(layout)
    total_cols = len(layout[0])

    while (current_row, current_col) != (end_row, end_col):
        if current_col < len(layout[current_row]) - 1:
            current_col += 1
            total_time += T_RIGHT
        elif current_row < total_rows - 1:
            current_row += 1
            current_col = 0
            total_time += T_RIGHT
        elif current_row == total_rows - 1:
            current_row = 0
            current_col = 0
            total_time += T_RIGHT

    return total_time + T_BLINK

def time_within_quadrant_left_path(layout, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    total_time = 0
    current_row, current_col = start_row, start_col
    total_rows = len(layout)
    total_cols = len(layout[0])

    while (current_row, current_col) != (end_row, end_col):
        if current_col > 0:
            current_col -= 1
            total_time += T_LEFT
        elif current_row > 0:
            current_row -= 1
            current_col = len(layout[current_row]) - 1  # Move to the last column of the previous row
            total_time += T_LEFT
        elif current_row == 0:
            current_row = total_rows -1
            current_col = len(layout[current_row]) - 1
            total_time += T_LEFT

    return total_time + T_BLINK


# Calculate the optimal time for all combinations of letters
import itertools

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'Space']
results = {}

for start_letter, end_letter in itertools.product(letters, repeat=2):
    start_pos = None
    end_pos = None

    if start_pos is None:
        start_pos = find_position(keyboard_layout, start_letter)

    if end_pos is None:
        end_pos = find_position(keyboard_layout, end_letter)
    
    if start_pos is None or end_pos is None:
        continue

    time_left = time_within_quadrant_left_path(keyboard_layout, start_pos, end_pos)
    time_right = time_within_quadrant_right_path(keyboard_layout, start_pos, end_pos)
    time = min(time_left, time_right)

    results[(start_letter, end_letter)] = time

# Print the results
for (start_letter, end_letter), time in results.items():
    print(f"Time from '{start_letter}' to '{end_letter}': {time:.2f} s")