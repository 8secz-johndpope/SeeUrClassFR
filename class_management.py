import boto3


def create_class(class_name):
    rekognition = boto3.client('rekognition', 'us-west-2')
    try:
        response = rekognition.create_collection(CollectionId=class_name)
        print('Curso ' + class_name + ' creado.')

    except Exception as e:
        print(e)
        print('Curso ' + class_name + ' ya existe.')


def get_name_s3(institution_bucket, key):
    s3 = boto3.client('s3')
    response = s3.head_object(
        Bucket=institution_bucket,
        Key=key
    )
    return response['Metadata']['fullname']


def update_index(institution_bucket, faceID, fullname):
    dynamodb = boto3.client('dynamodb')
    dynamodb.put_item(
        TableName=institution_bucket,
        Item={
            'RekognitionId': {'S': faceID},
            'FullName': {'S': fullname}
            })


def add_student_class(institution_bucket, class_name, student_name):
    rekognition = boto3.client('rekognition', 'us-west-2')
    # Agrega alumno al curso
    faceID = rekognition.index_faces(
        CollectionId=class_name,
        Image={
            'S3Object': {
                'Bucket': institution_bucket,  # institution name
                # Key del objeto S3 (alumno_nombre_apellido.png)
                'Name': student_name
            }
        }
    )  # Especifico que solo quiero el Face ID de la primera cara que reconozca
    FID = faceID['FaceRecords'][0]['Face']['FaceId']
    # Crea relacion Curso-Alumno por FaceId y Nombre Completo
    student_full_name = get_name_s3(institution_bucket, student_name)  # Entrega el valor
    update_index(institution_bucket, FID, student_full_name)
    print('Alumno ' + student_full_name + ' agregado al curso ' + class_name)
