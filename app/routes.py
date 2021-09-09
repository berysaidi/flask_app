from re import search
from json import loads
from app import app, cache
from app.schema import SCHEMA
from flask import request, redirect, jsonify, make_response
from jsonschema import validate
from werkzeug.exceptions import HTTPException
from jsonschema.exceptions import ValidationError
from json.decoder import JSONDecodeError
from cachetools import cached


# Caching Mac addresses to speedup retrieval
@cache.cached()
def read_macs():
    import csv
    with open("mac.csv", newline='') as f:
        reader = csv.reader(f, delimiter=',')
        macs = []
        for row in reader:
            macs.append(row[0])
        # get rid of title
        macs.pop(0)
        return macs


@app.route('/profiles/clientId:<mac>', methods=['POST'])
def index(mac):
    #check header 
    try:
        token = request.headers['x-authentication-token']
        clientId = request.headers['x-client-id']
    except KeyError:
        return make_response({'statusCode' : 401, 'error': 'Conflict' , 'message' : 'invalid clientId or token supplied'}), 401
    # TODO:
    # check clientID in db
    # check x-authentication-token
    if token != "BEARER token" or clientid != "client":
        return make_response({'statuscode' : 401, 'error': 'conflict' , 'message' : 'invalid clientid or token supplied'}), 401


    # check mac address format
    pattern = r"([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}"

    match = search(pattern, mac)
    if not match:
        return make_response({'statusCode' : 404, 'error': 'Not Found' , 'message' : 'profile of client %s does not exist' %mac }), 404
    
    macs = read_macs()
    if mac not in macs:
        return make_response({'statusCode' : 404, 'error': 'Not Found' , 'message' : 'profile of client %s does not exist' %mac }), 404


    try :
        data = loads(request.data)
        validate(instance=data, schema=SCHEMA)
    except ValidationError:
        return make_response({'statusCode' : 409, 'error': 'Conflict' , 'message' : 'data error' }), 409
    except JSONDecodeError:
        return make_response({'statusCode' : 409, 'error': 'Conflict' , 'message' : 'error unmarshalling json' }), 409
    
    # After all Validation is done, we can safely return a OK with the proper stuff
    return make_response(jsonify(data)), 200



# Exception Handler for uncaught errors to avoid embarassing ourselves !
@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now handling non-HTTP exceptions only
    return make_response({'statusCode' : 500, 'error': 'Internal Server Error' , 'message' : 'An internal server error occured' }), 500

