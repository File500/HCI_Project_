import keyboard
from open_camera import Camera
from open_keyboard import KeyB
from multiprocessing import Process

cam = Camera
keyb = KeyB

def loop_key():

    keyb.initialise()

def loop_camera():

   cam.open_and_run()

if __name__ == '__main__':

    Process(target=loop_key).start()

    Process(target=loop_camera).start()







