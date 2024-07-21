# Define time constants
T_RIGHT = 0.6
T_LEFT = 0.6
T_BLINK = 1.5

# Define quadrant layouts
quadrant_1_layout = [
    ["Quadrant 1", "Quadrant 2", "Quadrant 3", "Quadrant 4"],
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Backspace"],
    ["Caps Lock", "Space", "Enter"]
]
quadrant_2_layout = [
    ["Quadrant 1", "Quadrant 2", "Quadrant 3", "Quadrant 4"],
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "Backspace"],
    ["Caps Lock", "Space", "Enter"]
]
quadrant_3_layout = [
    ["Quadrant 1", "Quadrant 2", "Quadrant 3", "Quadrant 4"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l", "?", "Backspace"],
    ["Caps Lock", "Space", "Enter"]
]
quadrant_4_layout = [
    ["Quadrant 1", "Quadrant 2", "Quadrant 3", "Quadrant 4"],
    ["z", "x", "c", "v", "b", "n", "m", ",", ".", "!", "Backspace"],
    ["Caps Lock", "Space", "Enter"]
]

quadrants = [quadrant_1_layout, quadrant_2_layout, quadrant_3_layout, quadrant_4_layout]

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

def time_within_quadrant(layout, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    total_time = 0
    current_row, current_col = start_row, start_col
    total_rows = len(layout)
    total_cols = len(layout[0])

    while (current_row, current_col) != (end_row, end_col):
        if current_row == end_row:
            if current_col < end_col:
                current_col += 1
                total_time += T_RIGHT
            else:
                current_col -= 1
                total_time += T_LEFT
        else:
            if current_row < end_row:
                if current_col != total_cols - 1:
                    current_col += 1
                    total_time += T_RIGHT
                else:
                    current_row += 1
                    current_col = 0
                    total_time += T_RIGHT
            else:
                if current_col != 0:
                    current_col -= 1
                    total_time += T_LEFT
                else:
                    current_row -= 1
                    current_col = total_cols - 1
                    total_time += T_LEFT

    return total_time + T_BLINK


def time_between_quadrants(start_quadrant, end_quadrant, start_pos, end_pos):
    start_layout = quadrants[start_quadrant]
    end_layout = quadrants[end_quadrant]

    # Find the positions of the quadrant buttons
    quadrant_buttons = ["Quadrant 1", "Quadrant 2", "Quadrant 3", "Quadrant 4"]

    start_quadrant_button_pos = find_position(start_layout, quadrant_buttons[end_quadrant])
    end_quadrant_button_pos = find_position(end_layout, quadrant_buttons[0])  # After blinking, you're at "Quadrant 1"
    
    # Calculate time to quadrant button for both left and right paths
    time_to_quadrant_button_left = time_within_quadrant_left_path(start_layout, start_pos, start_quadrant_button_pos)
    time_to_quadrant_button_right = time_within_quadrant_right_path(start_layout, start_pos, start_quadrant_button_pos)

    # Choose the shorter path
    time_to_quadrant_button = min(time_to_quadrant_button_left, time_to_quadrant_button_right)

    # Calculate time from "Quadrant 1" button in the target quadrant to the target letter for both left and right paths
    time_from_first_quad_to_target_left = time_within_quadrant_left_path(end_layout, end_quadrant_button_pos, end_pos)
    time_from_first_quad_to_target_right = time_within_quadrant_right_path(end_layout, end_quadrant_button_pos, end_pos)

    # Choose the shorter path
    time_from_first_quad_to_target = min(time_from_first_quad_to_target_left, time_from_first_quad_to_target_right)
    
    return time_to_quadrant_button + time_from_first_quad_to_target

# Calculate the optimal time for all combinations of letters
import itertools

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'Space']
results = {}

for start_letter, end_letter in itertools.product(letters, repeat=2):
    start_quadrant, start_pos = None, None
    end_quadrant, end_pos = None, None

    for idx, layout in enumerate(quadrants):
        if start_pos is None:
            start_pos = find_position(layout, start_letter)
            if start_pos:
                start_quadrant = idx
        if end_pos is None:
            end_pos = find_position(layout, end_letter)
            if end_pos:
                end_quadrant = idx
        if start_pos and end_pos:
            break

    if start_quadrant == end_quadrant:
        time_left = time_within_quadrant_left_path(quadrants[start_quadrant], start_pos, end_pos)
        time_right = time_within_quadrant_right_path(quadrants[start_quadrant], start_pos, end_pos)
        time = min(time_left, time_right)
    else:
        time = time_between_quadrants(start_quadrant, end_quadrant, start_pos, end_pos)

    results[(start_letter, end_letter)] = time

# Print the results
for (start_letter, end_letter), time in results.items():
    print(f"Time from '{start_letter}' to '{end_letter}': {time:.2f} s")