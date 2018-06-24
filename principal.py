import boto3
from PIL import Image
import os
import os.path
import datetime
import class_table_managment as ctm
import student_management as sm
import class_management as cm


if __name__ == "__main__":
    institution_bucket = 'instituciondiegoportales'
    imageFile = './instituciondiegoportales/alumno_gustavo_gonzalez.jpg'
    class_name = 'tic3_1'
    student_name, _ = sm.pars_name(imageFile)
    print(student_name)
    #sm.add_student_s3(institution_bucket, imageFile)
    #cm.create_class(class_name)
    cm.add_student_class(institution_bucket, class_name, student_name)
