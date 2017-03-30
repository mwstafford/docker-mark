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

@app.route('/test1')
def test1():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('foot')

    #response = table.scan(
    #    FilterExpression=Attr('pick_user_id').lt(2)
    #)
    response = table.query(
        KeyConditionExpression=Key('pick_id').eq('228')
    )

    return json.dumps(response, indent=4, cls=DecimalEncoder)

@app.route('/test2')
def test2():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('foot')

    #response = table.scan(
    #    FilterExpression=Attr('pick_user_id').lt(2)
    #)
    response = table.query(
        KeyConditionExpression=Key('pick_id').eq('328')
    )

    return json.dumps(response, indent=4, cls=DecimalEncoder)

@app.route('/test3/<pick_id>', methods=['GET'])
def test3(pick_id):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('foot')
    response = table.query(
        KeyConditionExpression=Key('pick_id').eq(pick_id)
    )
    
    if len(response) == 0:
        abort(404)

    return json.dumps(response, indent=4, cls=DecimalEncoder)
    #return jsonify(response)

@app.route('/test4/<int:season_year>/<int:season_week>', methods=['GET'])
def test4(season_year, season_week):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('foot')
    response = table.scan(
        FilterExpression=Attr('season_year').eq(season_year)&Attr('season_week').eq(season_week)
    )
    
    if len(response) == 0:
        abort(404)

@app.route('/test5/<int:season_year>', methods=['GET'])
def test5(season_year):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('football')
    response = table.query(
        IndexName='season_year-season_week-index',
        KeyConditionExpression=Key('season_year').eq(season_year)
    )

    if len(response) == 0:
        abort(404)


    return json.dumps(response, indent=4, cls=DecimalEncoder)
    #return json.dumps(response, indent=4)
    #return jsonify(response)

@app.route('/test6', methods = ['POST'])
def api_message():

    if request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)

    else:
        return "415 Unsupported Media Type ;)"

@app.route('/test7', methods = ['POST'])
def test7():

    if request.headers['Content-Type'] == 'application/json':
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb.Table('football')
        #pick_id = int(1000)
        #season_year = int(2017)
        #return "JSON Message: " + json.dumps(request.json)
        #content = json.dumps(request.json)
        #content = json.loads(request.json)
        #response = table.put_item(Item=request.json))
        #return response

        #bets = json.loads(request.json)
        content = request.get_json()
            #season_year = int(bet['season_year'])
            #season_week = int(bet['season_week'])
   
        pick_id = int(content['pick_id'])
        season_year = int(content['season_year'])
        picked_team_name = content['picked_team_name']
        opposing_team_name = content['opposing_team_name']
        line_picked_team = content['line_picked_team']
        season_week = int(content['season_week'])
        wager = int(content['wager'])
        pick_user_id = int(content['pick_user_id'])

        table.put_item(
            Item={
               'pick_id': pick_id,
               'season_year': season_year,
               'picked_team_name': picked_team_name,
               'opposing_team_name': opposing_team_name,
               'line_picked_team': line_picked_team,
               'season_week': season_week,
               'wager': wager,
               'pick_user_id': pick_user_id,
            }
        )
        return "ok"
       
    else:
        return "415 Unsupported Media Type ;)"

@app.route('/test8', methods = ['POST'])
def test8():

    if request.headers['Content-Type'] == 'application/json':
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb.Table('football')
        content = request.get_json()

        for row in content:
            uuidpart1 = row['pick_id']
            uuidpart2 = uuid.uuid4()
            uuidfull = str(uuidpart1) + str(uuidpart2)
            table.put_item(
                Item={
                    'pick_id': uuidfull,
                    'season_year': int(row['season_year']),
                    'picked_team_name': row['picked_team_name'],
                    'opposing_team_name': row['opposing_team_name'],
                    'line_picked_team': row['line_picked_team'],
                    'season_week': int(row['season_week']),
                    'wager': int(row['wager']),
                    'pick_user_id': int(row['pick_user_id']),
                }
            )
        return "ok"        

    else:
        return "415 Unsupported Media Type ;)"


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
