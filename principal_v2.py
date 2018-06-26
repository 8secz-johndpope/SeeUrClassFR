import boto3
import os
import os.path
from PIL import Image
#from picamera import picamera
from time import sleep
import assistance_table_managment as atm
import student_management as sm
import class_management as cm
import face_identificaction as fid

if __name__ == "__main__":
    institution_bucket = 'instituciondiegoportales'
    class_name = 'tic3_1'
    path = './'+institution_bucket+'_test/'
    valid_images = [".jpg"]
    file_list = os.listdir(path)
    for photo_path in file_list:
        ext = os.path.splitext(photo_path)[1]
        if ext.lower() not in valid_images:
            continue
        fid.verify_face(institution_bucket, class_name,
                        Image.open(path+photo_path)
        #Error sucede en la linea 90 de atm: dynamoDB no tiene un atributo ni funcion llamado "Table"
        os.remove(path+photo_path)
                        #Image.open(os.path.join(path, photo_path)))
        #os.remove(os.path.join(path, photo_path)) Estos dos me estaban dando error antes, pero los guarde por si acaso
