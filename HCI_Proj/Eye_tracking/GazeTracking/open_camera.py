import mouse
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
        rest_y = (max_y / 3)*2 
        
        cursorX = rest_x
        cursorY = rest_y
        
        sum_x = 327
        sum_y = 208
        up_down_lim = 195 #210 for camera up and key down, 195 for free roam
        right_left_lim = 335 #320 for camera up and key down, 335 for free roam 
        
        global_timer_start = time.time()
        allow_blink = False
        
        step = 15
        
        moving_boundry = 620000
        error_rate = 400
        
        pyautogui.FAILSAFE = False

        while True:
            
            global_timer_end = time.time()
            
            if global_timer_end - global_timer_start > 1.3:
                allow_blink = True
            # We get a new frame from the webcam
            _, frame = webcam.read()

            # We send this frame to GazeTracking to analyze it
            gaze.refresh(frame)

            frame = gaze.annotated_frame()

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
                
            '''
            if cursorY > rest_y and cursorY < max_y and cursorX < max_x and cursorX > 0:
                
                pyautogui.moveTo(cursorX,cursorY)
            else:
                cursorX = rest_x
                cursorY = rest_y + 200
            '''
            pyautogui.moveTo(cursorX,cursorY)
            
            if gaze.is_blinking() and allow_blink and 1==0: 
                counter = 0
                flag_success = 0
                start = time.time()
                end = time.time()
                
                while end - start < 0.5 and gaze.is_blinking():
                    counter += 1
                    end = time.time()
                
                if counter > moving_boundry:
                    flag_success = 1
                    mouse.click('left')
                
                #print("before change counter:",counter,"average:",moving_boundry)
                
                if flag_success == 0:
                    moving_boundry = min(counter-error_rate, moving_boundry)     
                else:
                    moving_boundry = max(counter, moving_boundry+error_rate)
                
                #print("after change counter:",counter,"average:",moving_boundry)                          
                allow_blink = False
                global_timer_start = time.time()
            
            if(keyboard.is_pressed("esc")):
                break
    
        webcam.release()
        cv2.destroyAllWindows()
