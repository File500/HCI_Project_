"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
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
        looking_cord_x = 0
        looking_cord_y = 0

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

            if(gaze.horizontal_ratio()):
                looking_cord_x = max_x * gaze.horizontal_ratio()
            if(gaze.vertical_ratio()):
                looking_cord_y = max_y * gaze.vertical_ratio()
            cv2.imshow("Demo", frame)

            print("on screen pos x:", looking_cord_x, "on screen pos y:", looking_cord_y)

            if(keyboard.is_pressed("esc")):
                break
    
        webcam.release()
        cv2.destroyAllWindows()
