from picamera import PiCamera
from time import sleep
import take_distance as tdis


camera = PiCamera()
institution_bucket = 'instituciondiegoportales'
path = './'+institution_bucket+'_test/'
i = 0
while True:
    file_path = path + 'image{}.jpg'.format(i)
    distance = tdis.ReadDistance(11)
    if distance < 200:
        print("distancia: ", distance)
        print("Imagen", file_path)
        camera.capture(file_path)
        sleep(1)
        i += 1
