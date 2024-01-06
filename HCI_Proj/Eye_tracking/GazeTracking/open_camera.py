import time
import pyautogui
import keyboard
import ctypes
import cv2
from gaze_tracking import GazeTracking

class Camera(object):
    
    def open_and_run():
        gaze = GazeTracking()
        webcam = cv2.VideoCapture(0)

        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        max_x = screensize[0]
        max_y = screensize[1]
        rest_x = max_x / 2
        rest_y = max_y / 2 
        
        cursorX = rest_x
        cursorY = rest_y
        
        sum_x = 327
        sum_y = 208
        up_down_lim = 190
        right_left_lim = 332 
        
        global_timer_start = time.time()
        start = time.time()
        end = time.time()
        allow_blink = False
        
        step = 7
        
        blinking_lim = 0.5
                
        pyautogui.FAILSAFE = False

        while True:
            
            global_timer_end = time.time()
            
            if global_timer_end - global_timer_start > 1.3:
                allow_blink = True
            # We get a new frame from the webcam
            _, frame = webcam.read()

            # We send this frame to GazeTracking to analyze it
            gaze.refresh(frame)

            left_pupil = gaze.pupil_left_coords()
            right_pupil = gaze.pupil_right_coords()
            
            if left_pupil and right_pupil:
                sum_x = round((left_pupil[0] + right_pupil[0]) / 2)
                sum_y = round((left_pupil[1] + right_pupil[1]) / 2)
                
            if sum_x > right_left_lim:
                cursorX -= step
            elif sum_x < right_left_lim:
                cursorX += step
                
            if sum_y > up_down_lim:
                cursorY += step
            elif sum_y < up_down_lim:
                cursorY -= step
                
            pyautogui.moveTo(cursorX,cursorY)
    
            if gaze.is_blinking() and allow_blink: 
                
                end = time.time()
            else:
                start = time.time()
                
            if end - start >= blinking_lim:
                time.sleep(1)
                start = time.time()
                allow_blink = False
                global_timer_start = time.time()
                pyautogui.click(cursorX, cursorY)  
                
                
            if(keyboard.is_pressed("esc")):
                break
    
        webcam.release()
        cv2.destroyAllWindows()
