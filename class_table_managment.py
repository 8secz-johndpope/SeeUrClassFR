from __future__ import print_function  # Python 2/3 compatibility
import boto3
from boto3.dynamodb.conditions import Key, Attr


def create_table_class(class_name):
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
consult_asistance('tics3', 'asistencia_curso')
