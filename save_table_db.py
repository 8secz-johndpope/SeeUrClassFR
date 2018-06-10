from __future__ import print_function  # Python 2/3 compatibility
import boto3


def save_asistance_register(data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('asistencia_curso')
    print("Agregando valores a tabla: ", data)
    table.put_item(
        Item={
            'id': 'id',
            'curso': data['curso'],
            'nombre': data['nombre'],
            'fecha': data['fecha'],
            'hora': data['hora'],
            'rekog_value': data['rekog_value']
            }
        )
