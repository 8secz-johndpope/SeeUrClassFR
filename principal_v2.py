import boto3
import os
import os.path
from PIL import Image
from time import sleep
import schedule
import time
import assistance_table_managment as atm
import student_management as sm
import class_management as cm
import face_identificaction as fid


blocks = {
    'a': '8:00, 9:50',
    'b': '10:00, 11:20',
    'c': '11:30, 12:50',
    'd': '14:00, 15:20',
    'e': '15:30, 16:50',
    'f': '17:00, 18:20',
    'g': '18:30, 19:50'
}


def get_students_class_day(class_name):
    student_list = fid.get_students_class(class_name)
    return student_list


def script(student_list):
    valid_images = [".jpg"]
    file_list = os.listdir(path)
    for photo_path in file_list:
        ext = os.path.splitext(photo_path)[1]
        if ext.lower() not in valid_images:
            continue
        student_list = fid.verify_face(class_name, Image.open(os.path.join(path, photo_path)), student_list)
        os.remove(os.path.join(path, photo_path))


if __name__ == "__main__":
    institution_bucket = 'instituciondiegoportales'
    class_name = 'tic3_v6'
    path = './'+institution_bucket+'_test/'
    student_list = get_students_class_day(class_name)
    schedule.every(1).minutes.do(script, student_list)
    #student_list = schedule.every(120).minutes.do(get_students_class_day(class_name))
    while True:
        schedule.run_pending()
        time.sleep(1)
