from picamera import PiCamera
from time import sleep
camera = PiCamera()
institution_bucket = 'instituciondiegoportales'
path = './'+institution_bucket+'_test/'
path_v2 = './instituciondiegoportales_test/image%s.jpg'
i = 0
while True:
    file_path = path + 'image{}.jpg'.format(i)
    print(file_path)
    sleep(5)
    camera.capture(file_path)
    i += 1
    

