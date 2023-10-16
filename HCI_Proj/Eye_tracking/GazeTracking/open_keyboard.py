from tkinter import *
import os

root = Tk()

def callback(event):
    # so the touch keyboard is called tabtip.exe and its located in C:\Program Files\Common Files\microsoft shared\ink
    # here we run it after focus
    os.system("C:\\PROGRA~1\\COMMON~1\\MICROS~1\\ink\\tabtip.exe")

frame = Frame(root, width=100, height=100)
frame.pack()

addressInput = Entry(frame, font = "Verdana 20 ", justify="center")
addressInput.bind("<FocusIn>", callback)
addressInput.pack()

root.mainloop()
os.system('wmic process where name="TabTip.exe" delete') 