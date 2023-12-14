import tkinter as tk
from gaze_tracking import GazeTracking
import cv2
import time
import threading
from pynput.keyboard import Key, Controller


keyboard_layouts = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Backspace"],
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "Enter"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l", "?"],
    ["z", "x", "c", "v", "b", "n", "m", ",", ".", "!", "Caps Lock"]
]

all_keys = []
current_key_index = (0, 0)
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
kb = Controller()
highlighted_key = None
gaze_thread_running = True

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
    global all_keys
    all_keys = []  # Reset the all_keys list

    # Add keys from the special frame
    special_keys = []
    for widget in specialFrame.winfo_children():
        if isinstance(widget, tk.Button):
            special_keys.append(widget)
    all_keys.append(special_keys)

    # Add keys from the main frame
    main_keys = []
    for widget in mainFrame.winfo_children():
        if isinstance(widget, tk.Button):
            main_keys.append(widget)
    all_keys.append(main_keys)

    # Add keyboard keys
    keyboard_keys = []
    for widget in keyboard_frame.winfo_children():
        if isinstance(widget, tk.Button):
            keyboard_keys.append(widget)
    all_keys.append(keyboard_keys)



def refresh_keyboard():
    button_width = 6
    button_height = 3

    for row, row_keys in enumerate(keyboard_layouts):
        for col, key in enumerate(row_keys):
            if key == "Backspace" or key == "Enter" or key == "Caps Lock":
                key_button = tk.Button(specialFrame, text=key, width=button_width*4, height=button_height, command=lambda k=key: on_key_press(k), font=('Arial', 16))
                key_button.grid(row=row, column=0, sticky="nsew")
            else: 
                key_button = tk.Button(mainFrame, text=key, width=button_width, height=button_height, command=lambda k=key: on_key_press(k), font=('Arial', 16))
                key_button.grid(row=row, column=col, sticky="nsew")

    key_sp = tk.Button(keyboard_frame, text="Space", width=button_width*11, height=button_height, command=lambda k="Space": on_key_press(k), font=('Arial', 16))
    key_sp.grid(row=1,column=1)
    
    # Center the keyboard using row and column weights
    for i in range(len(keyboard_layouts) + 1):
        root.grid_rowconfigure(i, weight=1)
    for i in range(11):
        root.grid_columnconfigure(i, weight=1)

    merge_keys()
    all_keys.append([key_sp])


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
            if elapsed_time_blink >= 2.0:
                print("User has been blinking for 2 seconds")
                press_current_key()
                start_time_blink = time.time()

        else:
            start_time_left = None
            start_time_right = None
            start_time_blink = None



def gaze_tracking_thread():
    gaze = GazeTracking()  # Initialize gaze tracking
    webcam = cv2.VideoCapture(0)  # Replace 0 with the appropriate camera index if needed

    check_time_looking(gaze, webcam)


def main():
    global root,keyboard_frame, gaze_thread_running, gaze_tracking_thread, specialFrame, mainFrame


    # Start the gaze tracking thread
    gaze_tracking_thread = threading.Thread(target=gaze_tracking_thread)
    gaze_tracking_thread.start()


    root = tk.Tk()
    root.attributes('-topmost', True)
    root.title("Virtual Keyboard")

    # Configure dark theme
    root.tk_setPalette(background='#333', foreground='#fff', activeBackground='#444', activeForeground='#fff')
    root.geometry("1450x650")
    mainFrame = tk.Frame(root, height=1200, width=500, bg="gray")
    mainFrame.grid(row=0,column=1)
    specialFrame = tk.Frame(root, height=600, width=500, bg="gray")
    specialFrame.grid(row=0,column=2)

    keyboard_frame = tk.Frame(root)
    keyboard_frame.grid(row=2, column=0, columnspan=10, padx=10, pady=10)
    refresh_keyboard()
    select_key((0,0))

    root.mainloop()

    gaze_thread_running = False
    gaze_tracking_thread.join()

if __name__ == "__main__":
    main()