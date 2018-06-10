from __future__ import print_function  # Python 2/3 compatibility
import boto3
from boto3.dynamodb.conditions import Key, Attr

def consult_asistance():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('asistencia_curso')
    response = table.query(KeyConditionExpression=Key('curso').eq('tics3'))
    items = response['Items']
    print(items)


consult_asistance()