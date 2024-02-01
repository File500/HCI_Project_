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
    special_keys = {
        "Backspace": Key.backspace,
        "Enter": Key.enter,
        "Space": Key.space,
        "Caps Lock": Key.caps_lock,
        "Quadrant 1": lambda: on_quadrant_click(0),
        "Quadrant 2": lambda: on_quadrant_click(1),
        "Quadrant 3": lambda: on_quadrant_click(2),
        "Quadrant 4": lambda: on_quadrant_click(3)
    }

    if key in special_keys:
        action = special_keys[key]
        if callable(action):
            root.after(10, action)
        else:
            root.after(10, kb.tap(action))
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

    if quadrant_buttons not in all_keys:
        all_keys.append(quadrant_buttons)

    # List of frames to iterate over
    frames = [keyboard_frame, bottom_row_frame]

    for frame in frames:
        frame_keys = [widget for widget in frame.winfo_children() if isinstance(widget, tk.Button)]
        all_keys.append(frame_keys)

    # Add quadrant buttons
    all_keys.append(quadrant_buttons)


def create_button(parent, text, width, height, command, font):
    return tk.Button(parent, text=text, width=width, height=height, command=command, font=font)

def refresh_keyboard():
    global bottom_row_frame 
    for widget in keyboard_frame.winfo_children():
        widget.destroy()

    row_layout = keyboard_layouts[current_quadrant]
    row = 0
    for key_row in row_layout:
        col = 0
        for key in key_row:
            if key != " ":
                key_button = create_button(keyboard_frame, key, 5, 2, lambda k=key: on_key_press(k), ('Arial', 16))
                key_button.grid(row=row, column=col, padx=2, pady=2)
            col += 1

        backspace_button = create_button(keyboard_frame, "Backspace", 10, 2, lambda k="Backspace": on_key_press(k), ('Arial', 16))
        backspace_button.grid(row=row, column=col, columnspan=10, padx=10, pady=10)
        row += 1

    bottom_row_frame = tk.Frame(keyboard_frame)
    bottom_row_frame.grid(row=row, column=0, columnspan=col, padx=10, pady=10)

    left_label = tk.Label(bottom_row_frame, width=23)
    left_label.pack(side=tk.LEFT, expand=True)

    special_keys = {"Caps Lock": 10, "Space": 30, "Enter": 10}
    for key, width in special_keys.items():
        button = create_button(bottom_row_frame, key, width, 2, lambda k=key: on_key_press(k), ('Arial', 16))
        button.pack(side=tk.LEFT, padx=10, pady=10)

    row += 1
    merge_keys()

def check_time_looking(gaze, webcam, threshold_seconds=0.6):
    states = {
        "left": {"start_time": None, "elapsed_time": 0, "action": move_left, "message": "User has been looking left for 1 second"},
        "right": {"start_time": None, "elapsed_time": 0, "action": move_right, "message": "User has been looking right for 1 second"},
        "blinking": {"start_time": None, "elapsed_time": 0, "action": press_current_key, "message": "User has been blinking for 2 seconds", "threshold": 1.5}
    }

    while gaze_thread_running:
        _, frame = webcam.read()
        gaze.refresh(frame)

        for state, info in states.items():
            if getattr(gaze, f"is_{state}")():
                # Reset the other states
                for other_state in states:
                    if other_state != state:
                        states[other_state]["start_time"] = None

                if info["start_time"] is None:
                    info["start_time"] = time.time()
                else:
                    info["elapsed_time"] = time.time() - info["start_time"]

                if info["elapsed_time"] >= info.get("threshold", threshold_seconds):
                    print(info["message"])
                    info["action"]()
                    info["start_time"] = time.time()
            else:
                info["start_time"] = None
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