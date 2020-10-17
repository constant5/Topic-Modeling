import boto3

# boto3 is the AWS SDK library for Python.
# We can use the low-level client to make API calls to DynamoDB.
client = boto3.client('dynamodb')# region_name='us-east-1')

try:
    resp = client.create_table(
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
