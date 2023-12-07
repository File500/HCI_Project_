from open_camera import Camera
from open_key import KeyB
from EyeTrackingKeyboard import left_right_k
from multiprocessing import Process

cam = Camera
keyb = KeyB
keylr = left_right_k

def loop_camera():

    cam.open_and_run()
    
def loop_key():
    
    keyb.run_ons_key()
    
def loop_key_LR():

    keylr.run_left_right()
    
if __name__ == '__main__':
    
    #Process(target=loop_key).start()
    
    Process(target=loop_key_LR).start()
    
    #Process(target=loop_camera).start()
