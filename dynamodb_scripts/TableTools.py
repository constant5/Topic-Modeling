import boto3
from boto3.dynamodb.conditions import Key
import time

# boto3 is the AWS SDK library for Python.
# The "resources" interface allow for a higher-level abstraction than the low-level client interface.
# More details here: http://boto3.readthedocs.io/en/latest/guide/resources.html

class dynamodb():
    
    def __init__(self):
        
        self.client = boto3.client('dynamodb')
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('reddit')


    def create_table(self):

        try:
            resp = self.client.create_table(
                TableName="reddit",
                # Declare your Primary Key in the KeySchema argument
                KeySchema=[
                    {
                        "AttributeName": "subreddit",
                        "KeyType": "HASH"
                    },
                    {
                        "AttributeName": "created_utc",
                        "KeyType": 'RANGE'
                    }
                ],
                # Any attributes used in KeySchema or Indexes must be declared in AttributeDefinitions
                AttributeDefinitions=[
                    {
                        "AttributeName": "subreddit",
                        "AttributeType": "S"
                    },
                    {
                        "AttributeName": "created_utc",
                        "AttributeType": "N"
                    },
                    
                ],
                # ProvisionedThroughput controls the amount of data you can read or write to DynamoDB per second.
                # You can control read and write capacity independently.
                ProvisionedThroughput={
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1
                }
            )
            print("Table created successfully!")
        except Exception as e:
            print("Error creating table:")
            print(e)

    def delete_table(self):
        try:
            resp = self.client.delete_table(
                TableName="reddit",
            )
            print("Table deleted successfully!")
        except Exception as e:
            print("Error deleting table:")
            print(e)


    def batch_writer(self):

        # The BatchWriteItem API allows us to write multiple items to a table in one request.
        with self.table.batch_writer() as batch:
            batch.put_item(Item={'subreddit': 'fffffffuuuuuuuuuuuu', 'created_utc': 1312156800, 'id': 'c298mtc', 
                'author': 'DorkyDude', 'body': '"$2, would you take that deal? I\'d take that deal"'} )
            batch.put_item(Item={'subreddit': 'motorcycles', 'created_utc': 1312156803, 'id': 'c298mtg', 
                'author': 'TrptJim', 'body': 'Have you wrecked in them yet?'} )
            batch.put_item(Item={'subreddit': 'reddevils', 'created_utc': 1312156801, 'id': 'c298mth', 
                'author': 'Migeycan87', 'body': 'I was thinking 170k max, but if we get another player off the books (Gibson) there would be a small bit more room to maneuver?'} )
            batch.put_item(Item={'subreddit': 'politics', 'created_utc': 1312156802, 'id': 'c298mti', 
                'author': 'chaon93', 'body': 'a baton is more likely to kill someone than a taser'} )
            batch.put_item(Item={'subreddit': 'WTF', 'created_utc': 1312156800,  'id': 'c298mtl', 
                'author': 'Typoking', 'body': 'Cut him a break, he probably just finished watching Training Day. '} )

    def query_items(self):
        # When making a Query API call, we use the KeyConditionExpression parameter to specify the hash key on which we want to query.
        resp = self.table.query(KeyConditionExpression=Key('subreddit').eq('politics'))

        print("The query returned the following items:")
        for item in resp['Items']:
            print(item)




