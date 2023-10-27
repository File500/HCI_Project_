from tkinter import *
import keyboard
import os

def callback(event):
        # so the touch keyboard is called tabtip.exe and its located in C:\Program Files\Common Files\microsoft shared\ink
        # here we run it after focus
        os.system("C:\\PROGRA~1\\COMMON~1\\MICROS~1\\ink\\tabtip.exe")

class KeyB(object):

    def initialise():
        root = Tk()
        root.attributes('-fullscreen',True)
        frame = Frame(root, width=100, height=100)
        frame.pack(padx=100,pady=100)

        addressInput = Entry(frame, font = "Verdana 20 ", justify="center")
        addressInput.bind("<FocusIn>", callback)
        addressInput.pack(padx=200,pady=200)
        
        button = Button(root, text="X", command=lambda: root.quit())
        button.pack(ipadx=5,ipady=5,expand=True)
        button.place(x=0,y=0)
        
        root.mainloop()
        os.system('wmic process where name="TabTip.exe" delete')
             
        
            