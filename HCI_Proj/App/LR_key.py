import tkinter as tk
from pynput.keyboard import Key, Controller


keyboard_layouts = [
    ["1234567890"],
    ["qwertyuiop"],
    ["asdfghjkl?"],
    ["zxcvbnm,.!"]
]

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

def on_quadrant_click(quadrant):
    global current_quadrant, highlighted_key
    current_quadrant = quadrant
    refresh_keyboard()
    #root.deiconify()  # Show the root window

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

def press_current_key():
    if highlighted_key:
        key = highlighted_key["text"]
        on_key_press(key)

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

def keybrd():
    global root, quadrant_buttons, keyboard_frame

    root = tk.Tk()
    root.attributes('-topmost', True)
    root.title("Virtual Keyboard")

    # Configure dark theme
    root.tk_setPalette(background='#333', foreground='#fff', activeBackground='#444', activeForeground='#fff')

    add_quadrant_buttons()
    configure_weights()

    keyboard_frame = tk.Frame(root)
    keyboard_frame.grid(row=2, column=0, columnspan=10, padx=10, pady=10)
    refresh_keyboard()
    

    root.mainloop()



