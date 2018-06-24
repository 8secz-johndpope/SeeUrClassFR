import boto3
import io
from PIL import Image

from s3Orders import conseguirNombreS3
from dynamoDBOrders import actualizarIndex, conseguirNombreDynamo
rekognition = boto3.client('rekognition','us-west-2')

def create_class(class_name):
    try:
        response = rekognition.create_collection(CollectionId=class_name)
        print('Curso ' + class_name + ' creado.')
    except Exception as e:
        print(e)
        print('Curso ' + class_name + ' ya existe de antemano.')


def retornarCurso(curso, tableName ='testtic3v2'):
    try:
        response = rekognition.list_faces(CollectionId=curso)['Faces']
    except Exception:
        print('ERROR: El curso ' + curso + ' no existe!')
        return {}

    allFaceIds = {}
    for element in response:
        allFaceIds[conseguirNombreDynamo(tableName, element['FaceId'])] = element['FaceId']
    
    return allFaceIds


def borrarCurso(curso):
    try:
        response = rekognition.delete_collection(CollectionId=curso)
        print('Curso ' + curso + ' eliminado!')
    except Exception as e:
        print(e)
        print('La tabla ' + curso + ' no existe!')

def agregarAlumnoCurso(tableName, curso, nombreAlumno):
    # Agrega alumno al curso
    faceID = rekognition.index_faces(
        CollectionId=curso,
        Image={
            'S3Object': {
                'Bucket': tableName, # institution name
                'Name': nombreAlumno # Key del objeto S3 (alumno_nombre_apellido.png)
            }
        }
    ) # Especifico que solo quiero el Face ID de la primera cara que reconozca
    FID = faceID['FaceRecords'][0]['Face']['FaceId']
    # Crea relacion Curso-Alumno por FaceId y Nombre Completo
    personFullName = conseguirNombreS3(tableName, nombreAlumno) # Entrega el valor 
    actualizarIndex(tableName, FID, personFullName)
    print('Alumno ' + personFullName + ' agregado al curso ' + curso)
    return


def borrarAlumnoCurso(tableName, curso, listaFaceIds):
    # Borrado de Alumnos
    response = rekognition.delete_faces(
        CollectionId = curso,
        FaceIds = listaFaceIds
    )

    # Aviso de que alumnos se borraron
    print('Los siguientes alumnos fueron borrado del curso '+ curso + ':')
    for elemento in listaFaceIds:
        nombre = conseguirNombreDynamo(tableName, elemento)
        print('- ' + nombre)
    return 


def comprarConColleccion(curso, imageFile):
    # Pasar imagen a blob
    
    image = imageFile
    
    stream = io.BytesIO()
    image.save(stream, format = 'JPEG')
    encodedimg = stream.getvalue()
    # Conseguir las cajas envolvientes de cada cara detectada
    response = rekognition.detect_faces(Image={'Bytes': encodedimg})
    allFaces = response['FaceDetails']
    allFaceIds = {} # Crea un diccionario {FaceId: Similarity}

    # Consigue proporciones del imagen entregado
    image_width = image.size[0]
    image_height = image.size[1]

    # Por cada cara detectada...
    for face in allFaces:
        # Crea un imagen temporal, que solo consiste en el area de la Caja Envolviente
        boundingBox = face['BoundingBox']
        x1 = int(boundingBox['Left'] * image_width) * 0.9
        y1 = int(boundingBox['Top'] * image_height) * 0.9
        x2 = int(boundingBox['Left'] * image_width + boundingBox['Width'] * image_width) * 1.1
        y2 = int(boundingBox['Top'] * image_height + boundingBox['Height'] * image_height) * 1.1

        croppredImage = image.crop((x1,y1,x2,y2))
        w = croppredImage.size[0]
        h = croppredImage.size[1]

        if w >= 80 and h >= 80:
            # Pasa este imagen temporal a un blob...
            stream = io.BytesIO()
            croppredImage.save(stream, format = 'JPEG')
            binary = stream.getvalue()

            # Para luego pasar este imagen singular por Search Faces by Image
            response = rekognition.search_faces_by_image(
                CollectionId = curso,
                Image = {'Bytes': binary},
                FaceMatchThreshold=70 # minimo nivel de aceptacion
            )
            if len(response['FaceMatches']) == 0:
                print('Alumno no del Curso Detectado')
            else:
                # Agrega FaceId y Similarity del sujeto encontrado al diccionario
                allFaceIds[response['FaceMatches'][0]['Face']['FaceId']] = response['FaceMatches'][0]['Similarity']
        else:
            print('Foto de la persona es muy chica, descartando...')
    
    return allFaceIds # Entrega diccionario de caras con su similitud


''' Vieja version de Compare, solo revisaba una cara en la imagen
def compare2Collection(curso,encodedimg):
    response = rekognition.search_faces_by_image(
        CollectionId=curso, # nombre del curso
        Image={'Bytes': encodedimg}, # imagen por analizar
        FaceMatchThreshold=10 # minimo nivel de aceptacion
    )

    outputIDs = {}
    for element in response['FaceMatches']:
        outputIDs[element['Face']['FaceId']] = element['Similarity']

    print(response)

    if len(response['FaceMatches']) != 0:
        return outputIDs
        #return response['FaceMatches'][0]['Face']['FaceId'], response['FaceMatches'][0]['Similarity']
    else:
        return {}
'''
