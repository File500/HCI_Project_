import tkinter as tk
from tkinter import *
from open_camera import Camera
from open_key import KeyB
from LR_key import keybrd 
from multiprocessing import Process

cam = Camera
keyb = KeyB

def loop_camera():

    cam.open_and_run()
    
def loop_key():
    
    keyb.run_ons_key()
    
def loop_key_LR():

    keybrd()

def loop_home():

    start_home()
    
def on_key_press(k):
    
    if k == 1 or k == 2:
        Process(target=loop_key_LR).start()
    
        #Process(target=loop_camera).start()
        
    if k == 3 or k == 4:
        Process(target=loop_key).start()
        
        #Process(target=loop_camera).start()
        
def start_home():
            
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.title("Home")
        
    key=[["Quadrant_key + Left_Right",
        "Quadrant_key + Free_Roam"],
        ["Qwerty + Left_Right",
         "Qwerty + Free_Roam"]]
    
    key_ind = [[1,2],[3,4]]
        
        # Calculate button width and height to make buttons the same size as Microsoft On-Screen Keyboard
    button_width = 6
    button_height = 3

        # Configure dark theme
    root.tk_setPalette(background='#333', foreground='#fff', activeBackground='#444', activeForeground='#fff')
    root.geometry("875x450")
    frame = tk.Frame(root, height=1000, width=1000, bg="gray")
    frame.grid(row=0, column=0)
    br = 1
        
    for i in range(2):
        for j in range(2):
            key_button = tk.Button(frame, text=key[i][j], width=button_width*4, height=button_height, command=lambda inde = key_ind[i][j]: on_key_press(inde), font=('Arial', 16))
            key_button.grid(row=i, column=j, sticky="nsew", padx=70, pady=70)
        
    root.mainloop()
    
if __name__ == '__main__':
    
    Process(target=loop_home).start()
