from open_camera import Camera
from open_input import Inp
from open_key import KeyB
from multiprocessing import Process


cam = Camera
inp = Inp
keyb = KeyB

def loop_inp():

    inp.initialise()

def loop_camera():

    cam.open_and_run()
    
def loop_key():
    
    keyb.run_ons_key()
    
if __name__ == '__main__':

    Process(target=loop_inp).start()
    
    Process(target=loop_key).start()
    
    #Process(target=loop_camera).start()
  







