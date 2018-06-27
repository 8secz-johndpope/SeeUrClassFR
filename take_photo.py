from picamera import PiCamera
from time import sleep


camera = PiCamera()
institution_bucket = 'instituciondiegoportales'
path = './'+institution_bucket+'_test/'
camera.capture(path + 'foto_test.jpg')
