import boto3
from boto3.dynamodb.conditions import Key, Attr


def create_table_class_assistance(class_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
        TableName = class_name,
        KeySchema = [
            {
                'AttributeName': 'curso',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'hora',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'curso',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'hora',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print("Table status:", table.table_status)


def get_name(class_name, face_id):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(
        TableName=class_name,
        Key={
            'RekognitionId': {
                'S': face_id,
            }
        },
        ProjectionExpression='FullName'
    )
    return response['Item']['FullName']['S']


def create_class_table(class_name):
    dynamodb = boto3.client('dynamodb')
    check_table = dynamodb.list_tables()
    #print(class_name, check_table['TableNames']) era para debug, ya no se necesita

    if len(check_table['TableNames']) == 0 or class_name not in check_table['TableNames']:
        response = dynamodb.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'RekognitionId',
                    'AttributeType': 'S'
                }
            ],
            TableName=class_name,
            KeySchema=[
                {
                    'AttributeName': 'RekognitionId',
                    'KeyType': 'HASH'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print('Dynamo Table ' + class_name + ' fue creada exitosamente!')
    else:
        print('La Tabla ' + class_name + ' ya existe!')


def delete_table(table_name):
    dynamodb = boto3.client('dynamodb')
    dynamodb.delete_table(TableName=table_name)
    

def save_asistance_register(table_name, data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name + 'assistance')
    print("Agregando valores a tabla: ", data)
    table.put_item(
        Item={
            'curso': data['curso'],
            'nombre': data['nombre'],
            'fecha': data['fecha'],
            'hora': data['hora'],
            'rekog_value': data['rekog_value']
        }
    )
    print("Done")
    

def consult_asistance(value, table_name):
    dynamodb = boto3.client('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.query(KeyConditionExpression=Key('curso').eq(value))
    items = response['Items']
    for item in items:
        print(item)
   
