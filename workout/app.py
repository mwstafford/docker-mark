from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import uuid
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


from flask import Flask, jsonify, request, make_response, abort

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

@app.route('/test2')
def test2():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('workout')

    #response = table.scan()
    #response = table.query(
        #KeyConditionExpression=Key('event_id').eq('123')
    #)
    response = table.scan(
        IndexName='user_id-event_timestamp-index'
    )
    #response = table.query(
        #IndexName='user_id-event_timestamp-index',
        #KeyConditionExpression=Key('event_id').BEGINS_WITH('mark')
    #)


    return json.dumps(response, indent=4, cls=DecimalEncoder)

@app.route('/test6', methods = ['POST'])
def test6():

    if request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)

    else:
        return "415 Unsupported Media Type ;)"

@app.route('/test3', methods = ['POST'])
def test3():

    if request.headers['Content-Type'] == 'application/json':
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb.Table('workout')
        content = request.get_json()

        for row in content:
            uuidpart1 = 'mark'
            uuidpart2 = uuid.uuid4()
            uuidfull = str(uuidpart1) + str(uuidpart2)
            table.put_item(
                Item={
                    'event_id': uuidfull,
                    'user_id': int(row['user_id']),
                    'event_timestamp': int(row['event_timestamp']),
                    'r_level': int(row['r_level']),
                    'event_time': row['event_time'],
                    'distance': row['distance'],
                }
            )
        return "ok"

    else:
        return "415 Unsupported Media Type ;)"



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
