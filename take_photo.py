from picamera import PiCamera
from time import sleep
camera = PiCamera
institution_bucket = 'instituciondiegoportales'
path = './'+institution_bucket+'_test/'
i = 0
while True:
    file_path = path + 'image{}.jpg'.format(i)
    camera.capture(file_path)
    i += 1
    sleep(5)

