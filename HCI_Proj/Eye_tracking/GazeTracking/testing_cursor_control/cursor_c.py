import ctypes
import pyautogui
import pygame
import keyboard
import mouse 
from pygame.locals import *

def main():
   
   pygame.init()
   pygame.display.set_mode((500,500))
   pygame.display.set_caption('Testing')
   running = True
   curr_pos = mouse.get_position()

   while running:

      if keyboard.is_pressed('space'):
            mouse.click('left')

      if (mouse.get_position != curr_pos):
            curr_pos = mouse.get_position()
            print('mouse position changed to:', mouse.get_position())   
            
      for event in pygame.event.get():
         if event.type == QUIT:
            running = False
         if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
         if event.type == MOUSEBUTTONDOWN:
           print(pygame.mouse.get_pos())

   pygame.display.quit()

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

print(screensize)
pyautogui.moveTo(0, 0)
print(mouse.get_position())

if __name__ == '__main__':
   main()
 
