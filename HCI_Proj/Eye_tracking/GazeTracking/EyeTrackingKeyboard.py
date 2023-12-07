import tkinter as tk
from gaze_tracking import GazeTracking
import cv2
import time
import threading

class left_right_k(object):
    
    def run_left_right():
        
        keyboard_layouts = [
            ["1234567890"],
            ["QWERTYUIOP"],
            ["ASDFGHJKL"],
            ["ZXCVBNM"]
        ]

        current_quadrant = 0
        current_key_index = (0, 0)
        gaze = GazeTracking()
        webcam = cv2.VideoCapture(0)

        highlighted_key = None

        def on_quadrant_click(quadrant):
            global current_quadrant, highlighted_key
            current_quadrant = quadrant
            highlighted_key = None  # Reset the highlighted key
            refresh_keyboard()
            select_key((0, 0))

        def on_key_press(key):
            entry.insert(tk.END, key)

        def clear_entry():
            current_text = entry.get()
            if current_text:
                updated_text = current_text[:-1]
                entry.delete(0, tk.END)
                entry.insert(0, updated_text)

        def select_key(key_index):
            global highlighted_key, current_key_index
            if highlighted_key:
                highlighted_key.configure(bg='#333', fg='#fff')  # Reset the previously highlighted key
            row, col = key_index
            key_button = keyboard_frame.grid_slaves(row=row, column=col)[0]
            key_button.configure(bg="yellow")  # Highlight the selected key
            highlighted_key = key_button
            current_key_index = key_index


        def press_current_key():
            if highlighted_key:
                key = highlighted_key["text"]
                on_key_press(key)

        def refresh_keyboard():
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
                backspace_button = tk.Button(keyboard_frame, text="<=", width=10, height=2, command=lambda k="<=": clear_entry(), font=('Arial', 16))
                backspace_button.grid(row=row, column=col, columnspan=10, padx=10, pady=10)
                row += 1


            # Add space button
            space_button = tk.Button(keyboard_frame, text="Space", width=30, height=2, command=lambda k=" ": on_key_press(k), font=('Arial', 16))
            space_button.grid(row=row, column=1, columnspan=10, padx=10, pady=10)
            row += 1


        root = tk.Tk()
        root.title("Virtual Keyboard")

        # Configure dark theme
        root.tk_setPalette(background='#333', foreground='#fff', activeBackground='#444', activeForeground='#fff')

        entry = tk.Entry(root, font=('Arial', 20), bg='#333', fg='#fff')
        entry.grid(row=0, column=0, columnspan=10, padx=10, pady=10)

        quadrant_buttons = []

        for i, quadrant in enumerate(keyboard_layouts):
            quadrant_button = tk.Button(root, text=f"Quadrant {i + 1}", width=10, height=2, command=lambda q=i: on_quadrant_click(q), font=('Arial', 16))
            quadrant_button.grid(row=1, column=i+3, padx=10, pady=10)
            quadrant_buttons.append(quadrant_button)

        # Configure row and column weights to make the quadrants expand
        for i in range(10):
            root.grid_rowconfigure(i, weight=3)
            root.grid_columnconfigure(i, weight=3)

        keyboard_frame = tk.Frame(root)
        keyboard_frame.grid(row=2, column=0, columnspan=10, padx=10, pady=10)
        refresh_keyboard()
        select_key((0,0))

        root.mainloop()
