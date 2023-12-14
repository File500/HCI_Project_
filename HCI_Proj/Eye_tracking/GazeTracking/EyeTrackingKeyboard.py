import tkinter as tk
from gaze_tracking import GazeTracking
import cv2
import time
import threading
from pynput.keyboard import Key, Controller


keyboard_layouts = [
    ["1234567890"],
    ["qwertyuiop"],
    ["asdfghjkl?"],
    ["zxcvbnm,.!"]
]

all_keys = []
current_quadrant = 0
current_key_index = (0, 0)
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
kb = Controller()
highlighted_key = None
quadrant_buttons = []
gaze_thread_running = True


def add_quadrant_buttons():
    global quadrant_buttons
    for i, quadrant in enumerate(keyboard_layouts):
        quadrant_button = tk.Button(root, text=f"Quadrant {i + 1}", width=10, height=2, command=lambda q=i: on_quadrant_click(q), font=('Arial', 16))
        quadrant_button.grid(row=1, column=i+3, padx=10, pady=10)
        quadrant_buttons.append(quadrant_button)

    all_keys.append(quadrant_buttons)

def on_quadrant_click(quadrant):
    global current_quadrant, highlighted_key
    current_quadrant = quadrant
    refresh_keyboard()
    select_key((0, 0))
    root.deiconify()  # Show the root window

# Configure row and column weights to make the quadrants expand
def configure_weights():
    for i in range(10):
        root.grid_rowconfigure(i, weight=3)
        root.grid_columnconfigure(i, weight=3)

def on_key_press(key):
    root.withdraw()
    if key == "Backspace":
        root.after(10, kb.tap(Key.backspace))
    elif key == "Enter":
        root.after(10, kb.tap(Key.enter)) 
    elif key == "Space":
        root.after(10, kb.tap(Key.space))
    elif key == "Caps Lock":
        root.after(10, kb.press(Key.caps_lock))
        root.after(10, kb.release(Key.caps_lock))
    elif key == "Quadrant 1":
        root.after(10, lambda: on_quadrant_click(0))
    elif key == "Quadrant 2":
        root.after(10, lambda: on_quadrant_click(1))
    elif key == "Quadrant 3":
        root.after(10, lambda: on_quadrant_click(2))
    elif key == "Quadrant 4":
        root.after(10, lambda: on_quadrant_click(3))
    else:
        root.after(10, kb.tap(key))
    root.deiconify()


def select_key(key_index):
    global highlighted_key, current_key_index
    if highlighted_key:
        highlighted_key.configure(bg='#333', fg='#fff')  # Reset the previously highlighted key
    row, col = key_index
    # Get total number of rows and columns
    total_rows = len(all_keys)
    total_cols = len(all_keys[row])
    print(total_rows, total_cols)

    # If the next key index is beyond the last column, reset the column to 0 and increment the row index
    if col >= total_cols:
        col = 0
        row += 1

    # If the row index is beyond the last row, reset it to 0
    if row >= total_rows:
        row = 0
        col = 0

    key_button = all_keys[row][col]
    key_button.configure(bg="yellow")  # Highlight the selected key
    highlighted_key = key_button
    current_key_index = (row, col)

def move_left():
    global current_key_index
    row, col = current_key_index
    if col > 0:
        col -= 1
    elif row > 0:  # If the current key is at the start of a row and it's not the first row
        row -= 1  # Move to the previous row
        col = len(all_keys[row]) - 1  # Move to the last key of the previous row
    select_key((row, col))

def move_right():
    global current_key_index
    row, col = current_key_index
    col += 1
    select_key((row, col))

def press_current_key():
    if highlighted_key:
        key = highlighted_key["text"]
        on_key_press(key)

def merge_keys():
    global all_keys, keyboard_frame, bottom_row_frame
    all_keys = []  # Reset the all_keys list

    # Add quadrant buttons
    if quadrant_buttons not in all_keys:
        all_keys.append(quadrant_buttons)

    # Add keyboard keys
    keyboard_keys = []
    for widget in keyboard_frame.winfo_children():
        if isinstance(widget, tk.Button):
            keyboard_keys.append(widget)
    all_keys.append(keyboard_keys)

    # Add bottom row buttons
    bottom_row_keys = []
    for widget in bottom_row_frame.winfo_children():
        if isinstance(widget, tk.Button):
            bottom_row_keys.append(widget)
    all_keys.append(bottom_row_keys)

    print(all_keys)


def refresh_keyboard():
    global bottom_row_frame 
    for widget in keyboard_frame.winfo_children():
        widget.destroy()

    row_layout = keyboard_layouts[current_quadrant]
    row = 0
    for key_row in row_layout:
        col = 0
        for key in key_row:
            if key == " ":
                col += 1
            else:
                key_button = tk.Button(keyboard_frame, text=key, width=5, height=2, command=lambda k=key: on_key_press(k), font=('Arial', 16))
                key_button.grid(row=row, column=col, padx=2, pady=2)
                col += 1
        # Add backspace button
        backspace_button = tk.Button(keyboard_frame, text="Backspace", width=10, height=2, command=lambda k="Backspace": on_key_press(k), font=('Arial', 16))
        backspace_button.grid(row=row, column=col, columnspan=10, padx=10, pady=10)
        row += 1


    # Create a new frame for the bottom row
    bottom_row_frame = tk.Frame(keyboard_frame)
    bottom_row_frame.grid(row=row, column=0, columnspan=col, padx=10, pady=10)

    # empty label to move buttons to the center of the frame
    left_label = tk.Label(bottom_row_frame, width=23)
    left_label.pack(side=tk.LEFT, expand=True)
    # Add Caps Lock button
    caps_lock_button = tk.Button(bottom_row_frame, text="Caps Lock", width=10, height=2, command=lambda k="Caps Lock": on_key_press(k), font=('Arial', 16))
    caps_lock_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Add space button
    space_button = tk.Button(bottom_row_frame, text="Space", width=30, height=2, command=lambda k=" ": on_key_press(k), font=('Arial', 16))
    space_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Add Enter button
    enter_button = tk.Button(bottom_row_frame, text="Enter", width=10, height=2, command=lambda k="Enter": on_key_press(k), font=('Arial', 16))
    enter_button.pack(side=tk.LEFT, padx=10, pady=10)
    row += 1
    merge_keys()

def check_time_looking(gaze, webcam, threshold_seconds=0.75):
    start_time_left = None
    start_time_right = None
    start_time_blink = None
    elapsed_time_left = 0
    elapsed_time_right = 0
    elapsed_time_blink = 0

    while gaze_thread_running:
        _, frame = webcam.read()
        gaze.refresh(frame)

        if gaze.is_left():
            # Reset the right gaze/blink timer
            start_time_right = None
            start_time_blink = None

            if start_time_left is None:
                start_time_left = time.time()
            else:
                elapsed_time_left = time.time() - start_time_left

            if elapsed_time_left >= threshold_seconds:
                print("User has been looking left for 1 second")
                move_left()
                start_time_left = time.time()

        elif gaze.is_right():
            # Reset the left gaze/blink timer
            start_time_left = None
            start_time_blink = None

            if start_time_right is None:
                start_time_right = time.time()
            else:
                elapsed_time_right = time.time() - start_time_right

            if elapsed_time_right >= threshold_seconds:
                print("User has been looking right for 1 second")
                move_right()
                start_time_right = time.time()
        elif gaze.is_blinking():
            start_time_left = None
            start_time_right = None

            if start_time_blink is None:
                start_time_blink = time.time()
            else: 
                elapsed_time_blink = time.time() - start_time_blink
            if elapsed_time_blink >= 2.2:
                print("User has been blinking for 2 seconds")
                press_current_key()
                start_time_blink = time.time()

        else:
            start_time_left = None
            start_time_right = None
            start_time_blink = None
    webcam.release()



def gaze_tracking_thread():
    gaze = GazeTracking()  # Initialize gaze tracking
    webcam = cv2.VideoCapture(0)  # Replace 0 with the appropriate camera index if needed

    check_time_looking(gaze, webcam)


def main():
    global root,quadrant_buttons, keyboard_frame, bottom_row_frame, gaze_thread_running, gaze_tracking_thread


    # Start the gaze tracking thread
    gaze_tracking_thread = threading.Thread(target=gaze_tracking_thread)
    gaze_tracking_thread.start()


    root = tk.Tk()
    root.title("Virtual Keyboard")

    # Configure dark theme
    root.tk_setPalette(background='#333', foreground='#fff', activeBackground='#444', activeForeground='#fff')


    add_quadrant_buttons()
    configure_weights()

    keyboard_frame = tk.Frame(root)
    keyboard_frame.grid(row=2, column=0, columnspan=10, padx=10, pady=10)
    refresh_keyboard()
    select_key((0,0))

    root.mainloop()

    gaze_thread_running = False
    gaze_tracking_thread.join()

if __name__ == "__main__":
    main()