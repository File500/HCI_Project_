from tkinter import *
import os

def callback(event):
        # so the touch keyboard is called tabtip.exe and its located in C:\Program Files\Common Files\microsoft shared\ink
        # here we run it after focus
        os.system("C:\\PROGRA~1\\COMMON~1\\MICROS~1\\ink\\tabtip.exe")

class KeyB(object):

    def initialise():
        
        root = Tk()
        root.attributes('-fullscreen',True)
        
        button = Button(root, text="X", command=lambda: root.quit())
        button.pack(ipadx=8,ipady=8,expand=True, side=TOP, anchor=NE)

        addressInput = Text(root, font = "Verdana 20 ", height=500)
        addressInput.bind("<FocusIn>", callback)
        addressInput.pack(padx=500,pady=500)
        
        root.mainloop()
        os.system('wmic process where name="TabTip.exe" delete')
             
        
            