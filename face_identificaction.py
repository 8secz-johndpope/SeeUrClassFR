import boto3
import io
import datetime
import assistance_table_managment as atm
from PIL import Image
rekognition = boto3.client('rekognition', 'us-west-2')


def prepare_faces(curso, imageFile):
    # Pasar imagen a blob
    image = imageFile
    stream = io.BytesIO()
    image.save(stream, format='JPEG')
    encodedimg = stream.getvalue()
    # Conseguir las cajas envolvientes de cada cara detectada
    response = rekognition.detect_faces(Image={'Bytes': encodedimg})
    allFaces = response['FaceDetails']
    allFaceIds = {}  # Crea un diccionario {FaceId: Similarity}
    # Consigue proporciones del imagen entregado
    image_width = image.size[0]
    image_height = image.size[1]

    # Por cada cara detectada...
    for face in allFaces:
        # Crea un imagen temporal, que solo consiste en el area de la Caja Envolviente
        boundingBox = face['BoundingBox']
        x1 = int(boundingBox['Left'] * image_width) * 0.9
        y1 = int(boundingBox['Top'] * image_height) * 0.9
        x2 = int(boundingBox['Left'] * image_width +
                 boundingBox['Width'] * image_width) * 1.1
        y2 = int(boundingBox['Top'] * image_height +
                 boundingBox['Height'] * image_height) * 1.1

        croppredImage = image.crop((x1, y1, x2, y2))
        w = croppredImage.size[0]
        h = croppredImage.size[1]

        if w >= 80 and h >= 80:
            # Pasa este imagen temporal a un blob...
            stream = io.BytesIO()
            croppredImage.save(stream, format='JPEG')
            binary = stream.getvalue()
            try:
                # Para luego pasar este imagen singular por Search Faces by Image
                response = rekognition.search_faces_by_image(
                    CollectionId=curso,
                    Image={'Bytes': binary},
                    FaceMatchThreshold=70  # minimo nivel de aceptacion
                )
                if len(response['FaceMatches']) == 0:
                    print('Alumno no del Curso Detectado')
                else:
                    # Agrega FaceId y Similarity del sujeto encontrado al diccionario
                    allFaceIds[response['FaceMatches'][0]['Face']['FaceId']] = response['FaceMatches'][0]['Similarity']
            except:
                print("No se detectan rostros en la imagen")           
        else:
            print('Foto de la persona es muy chica, descartando...')

    return allFaceIds  # Entrega diccionario de caras con su similitud



def pass_to_blob(image):
    stream = io.BytesIO()
    image.save(stream, format='JPEG')
    return stream.getvalue()


def multiple_face_detection(encodedimg):
    response = rekognition.detect_faces(Image={'Bytes': encodedimg})
    print(len(response['FaceDetails']))
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


def get_students_class(class_name):
    try:
        response = rekognition.list_faces(CollectionId=class_name)['Faces']
    except Exception:
        print('ERROR: El curso ' + class_name + ' no existe!')
        return {}
    allFaceIds = {}
    for element in response:
        allFaceIds[atm.get_name(class_name, element['FaceId'])] = False
    return allFaceIds


def verify_face(class_name, image, student_list):
    face_list = prepare_faces(class_name, image)
    now = datetime.datetime.now()
    date = [now.year, now.month, now.day]
    date_str = '-'.join(str(e) for e in date)
    hour = [now.hour, now.minute, now.second]
    hour_str = ':'.join(str(e) for e in hour)
    
    if face_list != {}:
        for faceId, value in face_list.items():
            name = atm.get_name(class_name, faceId)
            if student_list[name] == False:
                student_list[name] = True
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
    return student_list
