from open_camera import Camera
from open_key import KeyB
from multiprocessing import Process

cam = Camera
keyb = KeyB

def loop_camera():

    cam.open_and_run()
    
def loop_key():
    
    keyb.run_ons_key()
    
if __name__ == '__main__':
    
    Process(target=loop_key).start()
    
    Process(target=loop_camera).start()
  







