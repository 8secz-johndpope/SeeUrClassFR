from picamera import PiCamera
from time import sleep


def take_photo(i):
    camera = PiCamera()
    institution_bucket = 'instituciondiegoportales'
    path = './'+institution_bucket+'_test/'
    file_path = path + 'image{}.jpg'.format(i)
    camera.capture(file_path)
    camera.close()
    sleep(5)
