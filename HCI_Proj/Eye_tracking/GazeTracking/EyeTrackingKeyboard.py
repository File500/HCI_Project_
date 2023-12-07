import tkinter as tk
from pynput.keyboard import Key, Controller

class left_right_k(object):
    
    def run_left_right():
        
        keyboard_layouts = [
            ["1234567890"],
            ["QWERTYUIOP"],
            ["ASDFGHJKL?"],
            ["ZXCVBNM,.!"]
        ]

        global root, entry, quadrant_buttons, keyboard_frame
        quadrant_buttons = []
        all_keys = []
        current_quadrant = 0
        kb = Controller()
      
        def add_quadrant_buttons():
            global quadrant_buttons
            for i, quadrant in enumerate(keyboard_layouts):
                quadrant_button = tk.Button(root, text=f"Quadrant {i + 1}", width=10, height=2, command=lambda q=i: on_quadrant_click(q), font=('Arial', 16))
                quadrant_button.grid(row=1, column=i+3, padx=10, pady=10)
                quadrant_buttons.append(quadrant_button)

            all_keys.append(quadrant_buttons)

        def on_quadrant_click(quadrant):
            global current_quadrant
            current_quadrant = quadrant
            refresh_keyboard()

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

        def clear_entry():
            current_text = entry.get()
            if current_text:
                updated_text = current_text[:-1]
                entry.delete(0, tk.END)
                entry.insert(0, updated_text)

        def merge_keys():
            global all_keys
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
                backspace_button = tk.Button(keyboard_frame, text="Backspace", width=10, height=2, command=lambda k="<=": clear_entry(), font=('Arial', 16))
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

        root = tk.Tk()
        root.title("Virtual Keyboard")

            # Configure dark theme
        root.tk_setPalette(background='#333', foreground='#fff', activeBackground='#444', activeForeground='#fff')

        entry = tk.Entry(root, font=('Arial', 20), bg='#333', fg='#fff')
        entry.grid(row=0, column=0, columnspan=10, padx=10, pady=10)

        add_quadrant_buttons()
        configure_weights()

        keyboard_frame = tk.Frame(root)
        keyboard_frame.grid(row=2, column=0, columnspan=10, padx=10, pady=10)
        refresh_keyboard()

        root.mainloop()

 
