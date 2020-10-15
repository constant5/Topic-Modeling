import boto3

# boto3 is the AWS SDK library for Python.
# The "resources" interface allow for a higher-level abstraction than the low-level client interface.
# More details here: http://boto3.readthedocs.io/en/latest/guide/resources.html
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('reddit')


# The BatchWriteItem API allows us to write multiple items to a table in one request.
with table.batch_writer() as batch:
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



        




