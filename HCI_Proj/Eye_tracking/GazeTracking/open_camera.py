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
        
        cursorX = max_x / 2
        cursorY = max_y / 2
        
        sum_x = 326
        sum_y = 204

        while True:
            # We get a new frame from the webcam
            _, frame = webcam.read()

            # We send this frame to GazeTracking to analyze it
            gaze.refresh(frame)

            frame = gaze.annotated_frame()

            left_pupil = gaze.pupil_left_coords()
            right_pupil = gaze.pupil_right_coords()
            cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
            cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

            '''
            if(gaze.horizontal_ratio()):
                looking_cord_x = max_x * gaze.horizontal_ratio()
            if(gaze.vertical_ratio()):
                looking_cord_y = max_y * gaze.vertical_ratio()
            cv2.imshow("Demo", frame)

            print("on screen pos x:", looking_cord_x, "on screen pos y:", looking_cord_y)
            '''
            if left_pupil and right_pupil:
                sum_x = round((left_pupil[0] + right_pupil[0]) / 2)
                sum_y = round((left_pupil[1] + right_pupil[1]) / 2)
                
            if sum_x > 327:
                cursorX -= 8
            elif sum_x < 327:
                cursorX += 8
                
            if sum_y > 210:
                cursorY += 8
            elif sum_y < 210:
                cursorY -= 8
                
            pyautogui.moveTo(cursorX,cursorY)   
            #print('x', sum_x, 'y', sum_y)
                      
            if(keyboard.is_pressed("esc")):
                break
    
        webcam.release()
        cv2.destroyAllWindows()
