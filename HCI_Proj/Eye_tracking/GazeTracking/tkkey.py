import tkinter as tk
from tkinter import *
import keyboard as kb



class KeyB(object):

    def run_ons_key():
        
      

        keyboard_layout = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Backspace"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "Enter"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Space"],
            ["Z", "X", "C", "V", "B", "N", "M"]
        ]

        def on_key_press(key):
            if key == "Backspace":
                clear_entry()
            elif key == "Enter":
                entry.insert(tk.END, '\n')
            elif key == "Space":
                entry.insert(tk.END, ' ')
            else:
                entry.insert(tk.END, key)

        def clear_entry():
            current_text = entry.get()
            if current_text:
                updated_text = current_text[:-1]
                entry.delete(0, tk.END)
                entry.insert(0, updated_text)

        root = tk.Tk()
        root.title("Virtual Keyboard")

        # Calculate button width and height to make buttons the same size as Microsoft On-Screen Keyboard
        button_width = 6
        button_height = 3

        # Configure dark theme
        root.tk_setPalette(background='#333', foreground='#fff', activeBackground='#444', activeForeground='#fff')

        entry = tk.Entry(root, font=('Arial', 20), bg='#333', fg='#fff')
        entry.grid(row=0, column=0, columnspan=11, padx=10, pady=10, sticky="nsew")

        # Create the keyboard layout using a for loop
        for row, row_keys in enumerate(keyboard_layout):
            for col, key in enumerate(row_keys):
                key_button = tk.Button(root, text=key, width=button_width, height=button_height, command=lambda k=key: on_key_press(k), font=('Arial', 16))
                key_button.grid(row=row + 1, column=col, padx=2, pady=2, sticky="nsew")

        # Center the keyboard using row and column weights
        for i in range(len(keyboard_layout) + 1):
            root.grid_rowconfigure(i, weight=1)
        for i in range(11):
            root.grid_columnconfigure(i, weight=1)

        root.mainloop()

    