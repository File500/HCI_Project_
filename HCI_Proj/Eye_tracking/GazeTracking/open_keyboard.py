from tkinter import *
import os

def callback(event):
        #os.system("C:\\PROGRA~1\\COMMON~1\\MICROS~1\\ink\\tabtip.exe")
        #os.system('wmic process where name="TabTip.exe" delete') #za gasenje
        os.system("C:\\PROGRA~1\\COMMON~1\\MICROS~1\\ink\\tabtip.exe")

class Inp(object):

    def initialise():
        
        root = Tk()
        root.geometry("1260x500+100+100")
        
        button = Button(root, text="X", command=lambda: root.quit())
        button.pack(ipadx=8,ipady=8,expand=True, side=TOP, anchor=NE)

        addressInput = Text(root, font = "Verdana 20 ", height=20)
        addressInput.bind("<FocusIn>", callback)
        addressInput.pack(padx=50,pady=50)
                
        root.mainloop()
        os.system('wmic process where name="TabTip.exe" delete') #za gasenje
        
            