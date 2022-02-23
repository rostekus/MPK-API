import json
from kdtree import *
import boto3

s3 = boto3.client("s3")
bucket = "mpkapi"


def lambda_handler(event, context):

    key = "kdree.json"
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response["Body"]
    json_object = json.loads(content.read())

    lat = event["queryStringParameters"]["lat"]
    lnt = event["queryStringParameters"]["lnt"]

    loc = (float(lat), float(lnt))
    best = kdtree_closest_point(json_object, loc)
    stop = {}
    if best:

        stop["lat"] = best[0]
        stop["lnt"] = best[1]
        stop["name"] = best[2]

    responseObject = {}
    responseObject["statusCode"] = 200
    responseObject["headers"] = {}
    responseObject["headers"]["Content-Type"] = "application/json"
    responseObject["body"] = json.dumps(stop)

    # 4. Return the response object
    return responseObject
