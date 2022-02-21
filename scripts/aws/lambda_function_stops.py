import json

import boto3
s3 = boto3.client('s3')
bucket= 'mpkapi'

def lambda_handler(event, context):
    
    key = 'stops.json'
    response = s3.get_object(Bucket = bucket, Key = key)
    content = response['Body']
    json_object = json.loads(content.read())
    
    
    line = event['queryStringParameters']['line']
    
   
    
    # best = kdtree_closest_point(json_object, loc)
    
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps( json_object[line])

    # 4. Return the response object
    return responseObject
 

