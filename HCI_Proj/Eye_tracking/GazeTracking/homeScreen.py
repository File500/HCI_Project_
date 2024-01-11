import tkinter as tk
from tkinter import *
from multiprocessing import Process
from EyeTrackingKeyboard import main
from LeftRightStandardKeyboard import main as main2
from open_camera import Camera
from open_key import KeyB
from LR_key import keybrd 

root = None
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

def Quadrant_LR():
    main()

def Standard_LR():
    main2()

def on_key_press(k):
    global root
    root.iconify()

    if k == 1:
        Process(target=Quadrant_LR).start()
    elif k == 2:
        Process(target=Standard_LR).start()
    elif k == 3:
        Process(target=loop_key_LR).start()
        Process(target=loop_camera).start()
    elif k == 4:
        Process(target=loop_key).start()
        Process(target=loop_camera).start()
        
        
def start_home():
    global root 
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.title("Home")

    # Configure dark theme
    root.tk_setPalette(background='#333', foreground='#fff', activeBackground='#444', activeForeground='#fff')
    root.geometry("900x550")

    # Create a frame
    frame = tk.Frame(root, bg='#333')
    frame.pack(expand=True, fill='both')

    # Create a title
    title = tk.Label(frame, text="HCI Experiment: Text Input Using Eye Tracking", bg="#333", fg="#ddd", font=('Arial', 20))
    title.pack(pady=20)

    # Create buttons
    buttons = ["Test 1", "Test 2", "Test 3", "Test 4"]
    for i, button in enumerate(buttons, start=1):
        btn = tk.Button(frame, text=button, command=lambda k=i: on_key_press(k), font=('Arial', 16), width=20, height=2)
        btn.pack(pady=10)

    root.mainloop()
    
if __name__ == '__main__':
    Process(target=start_home).start()