from picamera import PiCamera
from time import sleep
def photo():
    camera = PiCamera
    institution_bucket = 'instituciondiegoportales'
    path = './'+institution_bucket+'_test/'
    while True:
        camera.capture(path)
        sleep(5)
