from __future__ import print_function  # Python 2/3 compatibility
import boto3
from boto3.dynamodb.conditions import Key, Attr


def create_table_class_assistance(class_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
        TableName = class_name,
        KeySchema = [
            {
                'AttributeName': 'curso',
                'KeyType': 'HASH'  # Partition key
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


def createDynamoTable(tableName):
    check_table = dynamodb.list_tables()
    print(tableName, tableCheck['TableNames'])

    if len(check_table['TableNames']) == 0 or tableName not in check_table['TableNames']:
        response = dynamodb.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'RekognitionId',
                    'AttributeType': 'S'
                }
            ],
            TableName=tableName,
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
        print('Dynamo Table ' + tableName + ' fue creada exitosamente!')
    else:
        print('La Tabla ' + tableName + ' ya existe!')


def delete_table(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.delete()
    return print("Tabla eliminada")


def save_asistance_register(data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('asistencia_curso')
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
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.query(KeyConditionExpression=Key('curso').eq(value))
    items = response['Items']
    for item in items:
        print(item)
   

#delete_table('asistencia_curso')
#create_table_class('asistencia_curso')
#consult_asistance('tics3', 'asistencia_curso')
