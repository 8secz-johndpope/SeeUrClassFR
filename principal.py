import boto3
import os
import os.path
import datetime
from PIL import Image
#from picamera import picamera
from time import sleep
import assistance_table_managment as atm
import student_management as sm
import class_management as cm


if __name__ == "__main__":
    institution_bucket = 'instituciondiegoportales'
    imageFile = './instituciondiegoportales/alumno_gustavo_gonzalez.jpg'
    class_name = 'tic3_1'
    student_name, _ = sm.pars_name(imageFile)
    print(student_name)
    #atm.delete_table(class_name)
    #sm.add_student_s3(institution_bucket, imageFile)
    #cm.create_class(class_name)
    #atm.create_class_table(class_name)
    cm.add_student_class(institution_bucket, class_name, student_name)
    
