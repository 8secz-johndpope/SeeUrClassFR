from __future__ import print_function
import boto3


def create_table_class(class_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
        TableName = class_name,
        KeySchema=[
            {
                'AttributeName': 'curso',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'curso',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print("Table status:", table.table_status)
