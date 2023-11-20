import tkinter as tk
from tkinter import *
from pynput.keyboard import Key, Controller

class KeyB(object):

    def run_ons_key():
        
        kb = Controller()

        keyboard_layout = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Backspace"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "Enter"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Space"],
            ["Z", "X", "C", "V", "B", "N", "M"]
        ]

        def on_key_press(key):
            
            root.withdraw()
            
            if key == "Backspace":
                root.after(10, kb.tap(Key.backspace))
                
            elif key == "Enter":
                root.after(10, kb.tap(Key.enter)) 
                
            elif key == "Space":
                root.after(10, kb.tap(Key.space))
        
            else:
                root.after(10, kb.tap(key))
                
            root.deiconify()
            
        

        root = tk.Tk()
        root.attributes('-topmost', True)
        root.title("Virtual Keyboard")
        
        # Calculate button width and height to make buttons the same size as Microsoft On-Screen Keyboard
        button_width = 6
        button_height = 3

        # Configure dark theme
        root.tk_setPalette(background='#333', foreground='#fff', activeBackground='#444', activeForeground='#fff')

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

    