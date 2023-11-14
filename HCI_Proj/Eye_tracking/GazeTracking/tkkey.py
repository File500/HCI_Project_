import tkinter as tk
from tkinter import *
import keyboard as kb



class KeyB(object):

    def run_ons_key():
        
      root = tk.Tk() 
      root.configure(background='Gray')
      root.geometry("1260x500")
      
      MainFrame = Frame(root, bg='Gray', bd=10, width=1250, height=490)
      MainFrame.grid(row=1, column=0, padx=30)
      
      keys = [['1','2','3','4','5','6','7','8','9','0','-','=','bcksp'],
              ['tab','q','w','e','r','t','y','u','i','o','p','[',']'],
              ['caps','a','s','d','f','g','h','j','k','l',';','"','enter'],
              ['shift','z','x','c','v','b','n','m',',','.','/','?','alt']]
      
      for i, key_row in enumerate(keys):
          for j, key in enumerate(key_row):
              tk.Button(MainFrame, text=key, width=9, height=2).grid(row=i,column=j,sticky='nesw') 
    
      tk.Button(root, text=' ', width=100, height=2).grid(row=5)
      
      root.mainloop()
    