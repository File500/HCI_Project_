import tkinter as tk
from tkinter import *
from pynput.keyboard import Key, Controller

class KeyB(object):

    def run_ons_key():
        
        kb = Controller()
        

        keyboard_layout = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Backspace"],
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "Enter"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l", "?",],
            ["z", "x", "c", "v", "b", "n", "m", ",", ".", "!", "Caps Lock"]
        ]

        def on_key_press(key):
            
            root.withdraw()
            
            if key == "Backspace":
                root.after(10, kb.tap(Key.backspace))
                
            elif key == "Enter":
                root.after(10, kb.tap(Key.enter)) 
                
            elif key == "Space":
                root.after(10, kb.tap(Key.space))

            elif key == "Caps Lock":
                if kb.pressed(Key.caps_lock):
                    root.after(10, kb.release(Key.caps_lock))
                else:
                    root.after(10, kb.press(Key.caps_lock))

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
        root.geometry("1450x650")
        mainframe = tk.Frame(root, height=1200, width=500, bg="gray")
        mainframe.grid(row=0,column=1)
        specialframe = Frame(root, height=600, width=500, bg="gray")
        specialframe.grid(row=0,column=2)
        # Create the keyboard layout using a for loop

        for row, row_keys in enumerate(keyboard_layout):
            for col, key in enumerate(row_keys):

                if key == "Backspace" or key == "Enter" or key == "Caps Lock":
                    key_button = tk.Button(specialframe, text=key, width=button_width*4, height=button_height, command=lambda k=key: on_key_press(k), font=('Arial', 16))
                    key_button.grid(row=row, column=0, sticky="nsew")

                else: 
                    key_button = tk.Button(mainframe, text=key, width=button_width, height=button_height, command=lambda k=key: on_key_press(k), font=('Arial', 16))
                    key_button.grid(row=row, column=col, sticky="nsew")

        key_sp = tk.Button(root, text="Space", width=button_width*11, height=button_height, command=lambda k="Space": on_key_press(k), font=('Arial', 16))
        key_sp.grid(row=1,column=1)
        
        # Center the keyboard using row and column weights
        for i in range(len(keyboard_layout) + 1):
            root.grid_rowconfigure(i, weight=1)
        for i in range(11):
            root.grid_columnconfigure(i, weight=1)

        root.mainloop()

    