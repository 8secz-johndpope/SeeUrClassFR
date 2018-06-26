import boto3
import io
import datetime
import assistance_table_managment as atm
from PIL import Image
rekognition = boto3.client('rekognition', 'us-west-2')

def prepare_faces(class_name, image):
    encodedimg = pass_to_blob(image)
    all_faces = multiple_face_detection(encodedimg)
    image_width, image_height = image.size[0], image.size[1]
    for face in all_faces:
        w, h, crop_image = separate_faces(face, image, image_width, image_height)
        binary = pass_to_blob(crop_image)
        if w >= 80 and h >= 80:
            return search_faces(binary, class_name)
        else:
            print("Imagen muy peuqueña, descartando...")


def pass_to_blob(image):
    stream = io.BytesIO()
    image.save(stream, format='JPEG')
    return stream.getvalue()


def multiple_face_detection(encodedimg):
    response = rekognition.detect_faces(Image={'Bytes': encodedimg})
    return response['FaceDetails']


def separate_faces(face, image, image_width, image_height):
    boundingBox = face['BoundingBox']
    x1 = int(boundingBox['Left'] * image_width) * 0.9
    y1 = int(boundingBox['Top'] * image_height) * 0.9
    x2 = int(boundingBox['Left'] * image_width +
                boundingBox['Width'] * image_width) * 1.1
    y2 = int(boundingBox['Top'] * image_height +
                boundingBox['Height'] * image_height) * 1.1
    crop_image = image.crop((x1, y1, x2, y2))
    return crop_image.size[0], crop_image.size[1], crop_image


def search_faces(binary, class_name):
    faces = {}
    response = rekognition.search_faces_by_image(
        CollectionId=class_name,
        Image={'Bytes': binary},
        FaceMatchThreshold=70
    )
    if len(response['FaceMatches']) == 0:
        print('Alumno no detectado en el curso')
    else:
        faces[response['FaceMatches'][0]['Face']['FaceId']
            ] = response['FaceMatches'][0]['Similarity']
    return faces


def verify_face(institution_bucket, class_name, image):
    face_list = prepare_faces(class_name, image)
    now = datetime.datetime.now()
    date = [now.year, now.month, now.day]
    date_str = '-'.join(str(e) for e in date)
    hour = [now.hour, now.minute, now.second]
    hour_str = ':'.join(str(e) for e in hour)
    if face_list != {}:
        for key, value in face_list.items():
            name = atm.get_name(institution_bucket, key)
            rekog_value = str(round(value, 3))
            data = {
                'curso': class_name,
                'nombre': name,
                'fecha': date_str,
                'hora': hour_str,
                'rekog_value': rekog_value
            }
            atm.save_asistance_register(class_name, data)
    else:
        print('No hubo coincidencia')
