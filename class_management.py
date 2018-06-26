import boto3
import assistance_table_managment as atm

def create_class(class_name):
    rekognition = boto3.client('rekognition', 'us-west-2')
    try:
        print("primera creacion")
        rekognition.create_collection(CollectionId=class_name)
        print("Segunda creacion")
        atm.create_class_table(class_name)
        print("Tercera creacion")
        atm.create_table_class_assistance(class_name + 'assistance')
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


def update_index(class_name, faceID, fullname):
    dynamodb = boto3.client('dynamodb')
    dynamodb.put_item(
        TableName=class_name,
        Item={
            'RekognitionId': {
                'S': faceID
            },
            'FullName': {
                'S': fullname
            }
        }
    )


def add_student_class(institution_bucket, class_name, student_name):
    rekognition = boto3.client('rekognition', 'us-west-2')
    faceID = rekognition.index_faces(
        CollectionId=class_name,
        Image={
            'S3Object': {
                'Bucket': institution_bucket,
                'Name': student_name
            }
        }
    )
    FID = faceID['FaceRecords'][0]['Face']['FaceId']
    student_full_name = get_name_s3(institution_bucket, student_name)
    update_index(class_name, FID, student_full_name)
    print('Alumno ' + student_full_name + ' agregado al curso ' + class_name)
